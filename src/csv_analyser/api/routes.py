from __future__ import annotations

import json as _json
import re
import shutil
import threading
from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from csv_analyser.models.schemas import (
    AskRequest,
    AskResponse,
    ChartGenerationRequest,
    ChartGenerationResponse,
    ChartListResponse,
    CsvUploadResponse,
    ExecutePlanRequest,
    ExecutePlanResponse,
    HealthResponse,
    ObjectivesResponse,
    ObjectivesUploadRequest,
    ObjectivesUploadResponse,
    ResponseToObjectivesResponse,
    InsightsGenerationResponse,
    InsightsResponse,
    ReportGenerationResponse,
    ReportResponse,
    SqlStatusResponse,
    SummaryResponse,
)
from csv_analyser.services.chart_service import (
    OUTPUT_DIR,
    generate_standard_charts,
    get_chart_path,
    list_chart_artifacts,
)
from csv_analyser.services.data_service import DATA_PATH, build_summary, load_dataset, read_csv_any_encoding
from csv_analyser.services.insight_service import MODEL as INSIGHTS_MODEL
from csv_analyser.services.insight_service import generate_insights_bundle, read_final_insights
from csv_analyser.services.objectives_service import MODEL as OBJECTIVES_MODEL
from csv_analyser.services.objectives_service import (
    OPENROUTER_BASE_URL,
    count_objectives,
    generate_response_to_objectives,
)
from csv_analyser.services.report_service import generate_report, read_report
from csv_analyser.services.dirty_service import save_dirty_report
from csv_analyser.services.sql_service import (
    SQL_DIR,
    generate_sql_catalog,
    run_tests_and_merge,
)


OBJECTIVES_PATH = DATA_PATH.parent.parent / "OBJECTIVES.md"
SQL_STATUS_PATH = OUTPUT_DIR / "sql" / ".status.json"
router = APIRouter()

# ── Pipeline cancellation state ───────────────────────────────────────────────
_pipeline_lock = threading.Lock()
_pipeline_running = False
_pipeline_cancel = threading.Event()


def _check_cancel() -> None:
    if _pipeline_cancel.is_set():
        raise RuntimeError("Pipeline cancelled.")


def _build_sql_catalog_bg(csv_path: Path, original_filename: str = "") -> None:
    """Background task: generate SQL catalog + run tests, updating status file throughout."""
    SQL_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if original_filename:
        (SQL_STATUS_PATH.parent / "original_csv.md").write_text(
            f"# Original CSV\n\n`{original_filename}`\n", encoding="utf-8"
        )
    SQL_STATUS_PATH.write_text(
        _json.dumps({"status": "running", "original_filename": original_filename}),
        encoding="utf-8",
    )
    try:
        df = read_csv_any_encoding(csv_path)
        _title_path, queries_path = generate_sql_catalog(df, csv_path)
        run_tests_and_merge(queries_path, csv_path)
        SQL_STATUS_PATH.write_text(
            _json.dumps({"status": "ready", "original_filename": original_filename}),
            encoding="utf-8",
        )
    except Exception as exc:
        SQL_STATUS_PATH.write_text(
            _json.dumps({"status": "error", "message": str(exc), "original_filename": original_filename}),
            encoding="utf-8",
        )


def _clear_output() -> None:
    """Delete all generated output so a fresh dataset starts clean."""
    for folder in (OUTPUT_DIR / "images", OUTPUT_DIR / "insights"):
        if folder.exists():
            for child in folder.iterdir():
                child.unlink() if child.is_file() else shutil.rmtree(child)
    for fname in ("report.md", "dirty.csv", "dirty_rows.md", "RESPONSE_TO_OBJECTIVES.md", "RESPONSE_TO_OBJECTIVES.html"):
        f = OUTPUT_DIR / fname
        if f.exists():
            f.unlink()
    # Reset SQL agent status so the UI shows "not started" for the new dataset
    if SQL_STATUS_PATH.exists():
        SQL_STATUS_PATH.unlink()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


def _safe_category_from_name(name: str) -> str:
    if name.startswith("overview_"):
        return "overview"
    if name.startswith("correlation_"):
        return "correlation"
    if name.startswith("distribution_"):
        return "distribution"
    if name.startswith("category_"):
        return "category"
    if name.startswith("time_series_"):
        return "time"
    return "other"


def _build_image_cards() -> list[dict[str, str]]:
    image_dir = OUTPUT_DIR / "images"
    image_cards: list[dict[str, str]] = []
    if image_dir.exists():
        for path in sorted(image_dir.glob("*.png")):
            image_cards.append(
                {
                    "name": path.name,
                    "category": _safe_category_from_name(path.stem),
                    "url": f"/output/images/{path.name}",
                }
            )
    return image_cards


@router.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "gallery.html",
        {"request": request, "charts": [], "images": [], "insights_model": INSIGHTS_MODEL, "objectives_model": OBJECTIVES_MODEL},
    )


@router.get("/output-images")
def output_images() -> list[dict[str, str]]:
    return _build_image_cards()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/sql-status", response_model=SqlStatusResponse)
def sql_status() -> SqlStatusResponse:
    """Returns the current status of the sql-agent workflow."""
    orig_csv_path = SQL_STATUS_PATH.parent / "original_csv.md"
    original_filename = ""
    if orig_csv_path.exists():
        try:
            parts = orig_csv_path.read_text(encoding="utf-8").split("`")
            if len(parts) >= 2:
                original_filename = parts[1]
        except Exception:
            pass
    if SQL_STATUS_PATH.exists():
        try:
            data = _json.loads(SQL_STATUS_PATH.read_text(encoding="utf-8"))
            status = data.get("status", "not_started")
            message = data.get("message", "")
            # Count queries from the catalog file if status is ready
            query_count = 0
            if status == "ready":
                for catalog in sorted((OUTPUT_DIR / "sql").glob("sql_queries_*.md")):
                    query_count = catalog.read_text(encoding="utf-8").count("\n## ")
                    break
            return SqlStatusResponse(status=status, message=message, query_count=query_count, original_filename=original_filename)
        except Exception:
            pass
    return SqlStatusResponse(status="not_started", original_filename=original_filename)


@router.post("/rerun-sql-catalog")
async def rerun_sql_catalog(background_tasks: BackgroundTasks) -> dict:
    """Re-trigger the SQL catalog build for the currently uploaded CSV."""
    if not DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="No CSV uploaded yet — upload a file first.")
    orig_csv_path = SQL_STATUS_PATH.parent / "original_csv.md"
    original_filename = ""
    if orig_csv_path.exists():
        try:
            parts = orig_csv_path.read_text(encoding="utf-8").split("`")
            if len(parts) >= 2:
                original_filename = parts[1]
        except Exception:
            pass
    background_tasks.add_task(_build_sql_catalog_bg, DATA_PATH, original_filename)
    return {"status": "running", "message": "SQL catalog rebuild started."}


@router.post("/upload/csv", response_model=CsvUploadResponse)
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> CsvUploadResponse:
    try:
        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only .csv files are accepted.")

        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        try:
            read_csv_any_encoding(BytesIO(content))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Malformed CSV: {exc}") from exc

        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_bytes(content)
        _clear_output()

        df = load_dataset(DATA_PATH)
        summary = build_summary(df)
        background_tasks.add_task(_build_sql_catalog_bg, DATA_PATH, file.filename or "")
        return CsvUploadResponse(
            message="CSV uploaded successfully and saved as data/data.csv.",
            dataset_path=str(DATA_PATH),
            row_count=summary["row_count"],
            column_count=summary["column_count"],
            missing_cells=summary["missing_cells"],
            missing_pct=summary["missing_pct"],
            description=summary["description"],
        )
    finally:
        await file.close()


@router.post("/upload/objectives", response_model=ObjectivesUploadResponse)
def upload_objectives(payload: ObjectivesUploadRequest) -> ObjectivesUploadResponse:
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Objectives content cannot be empty.")
    OBJECTIVES_PATH.write_text(payload.content, encoding="utf-8")
    return ObjectivesUploadResponse(
        message="OBJECTIVES.md saved successfully.",
        path=str(OBJECTIVES_PATH),
    )


@router.get("/objectives", response_model=ObjectivesResponse)
def get_objectives() -> ObjectivesResponse:
    content = OBJECTIVES_PATH.read_text(encoding="utf-8") if OBJECTIVES_PATH.exists() else ""
    return ObjectivesResponse(content=content, path=str(OBJECTIVES_PATH))


@router.post("/generate/response-to-objectives", response_model=ResponseToObjectivesResponse)
async def generate_response_to_objectives_endpoint() -> ResponseToObjectivesResponse:
    try:
        import asyncio
        artifacts = list_chart_artifacts()
        loop = asyncio.get_event_loop()
        out_path, html_path = await loop.run_in_executor(None, generate_response_to_objectives, artifacts)
        objectives_text = OBJECTIVES_PATH.read_text(encoding="utf-8") if OBJECTIVES_PATH.exists() else ""
        objectives_count = count_objectives(objectives_text)
        return ResponseToObjectivesResponse(
            message="RESPONSE_TO_OBJECTIVES.md generated successfully.",
            path=str(out_path),
            html_path=str(html_path),
            objectives_found=objectives_count,
            model_used=OBJECTIVES_MODEL,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Response generation failed: {exc}") from exc


@router.get("/response-to-objectives/download")
def download_response_to_objectives() -> FileResponse:
    from csv_analyser.services.objectives_service import RESPONSE_PATH
    if not RESPONSE_PATH.exists():
        raise HTTPException(status_code=404, detail="RESPONSE_TO_OBJECTIVES.md has not been generated yet.")
    return FileResponse(
        path=str(RESPONSE_PATH),
        media_type="text/markdown",
        headers={"Content-Disposition": 'attachment; filename="RESPONSE_TO_OBJECTIVES.md"'},
    )


@router.get("/response-to-objectives/download-html")
def download_response_to_objectives_html() -> FileResponse:
    from csv_analyser.services.objectives_service import RESPONSE_HTML_PATH
    if not RESPONSE_HTML_PATH.exists():
        raise HTTPException(status_code=404, detail="RESPONSE_TO_OBJECTIVES.html has not been generated yet.")
    return FileResponse(
        path=str(RESPONSE_HTML_PATH),
        media_type="text/html",
        headers={"Content-Disposition": 'attachment; filename="RESPONSE_TO_OBJECTIVES.html"'},
    )


@router.get("/summary", response_model=SummaryResponse)
def summary() -> SummaryResponse:
    try:
        df = load_dataset()
        return SummaryResponse(**build_summary(df))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to summarize dataset: {exc}") from exc


@router.post("/generate/charts", response_model=ChartGenerationResponse)
def generate_charts(payload: ChartGenerationRequest) -> ChartGenerationResponse:
    try:
        df = load_dataset()
        artifacts = generate_standard_charts(
            df,
            clean_output=payload.clean_output,
            write_png=payload.write_png,
        )
        return ChartGenerationResponse(
            charts_generated=len(artifacts),
            output_dir=str(OUTPUT_DIR),
            charts=artifacts,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Chart generation failed: {exc}") from exc


@router.post("/execute", response_model=ExecutePlanResponse)
def execute_plan(payload: ExecutePlanRequest) -> ExecutePlanResponse:
    global _pipeline_running
    with _pipeline_lock:
        if _pipeline_running:
            raise HTTPException(status_code=409, detail="Pipeline already running.")
        _pipeline_running = True
        _pipeline_cancel.clear()
    try:
        df = load_dataset()
        _check_cancel()
        artifacts = generate_standard_charts(
            df,
            clean_output=payload.clean_output,
            write_png=payload.write_png,
        )
        _check_cancel()
        save_dirty_report(df)
        _check_cancel()
        report_path = generate_report(df, artifacts)
        _check_cancel()
        insights_md_path, insights_html_path, _ = generate_insights_bundle(
            df, artifacts, cancel_event=_pipeline_cancel
        )
        # SQL catalog is built on upload — do not overwrite it here
        existing_titles = sorted(SQL_DIR.glob("sql_title.md"))
        existing_queries = sorted(SQL_DIR.glob("sql_queries_*.md"))
        sql_title_path = existing_titles[0] if existing_titles else SQL_DIR / "sql_title.md"
        sql_queries_path = existing_queries[0] if existing_queries else SQL_DIR / "sql_queries_.md"
        html_count = sum(1 for artifact in artifacts if artifact.format == "html")
        png_count = sum(1 for artifact in artifacts if artifact.format == "png")
        return ExecutePlanResponse(
            message="Pipeline completed.",
            charts_generated=len(artifacts),
            html_charts=html_count,
            png_charts=png_count,
            report_path=str(report_path),
            insights_path=str(insights_md_path),
            insights_html_path=str(insights_html_path),
            sql_title_path=str(sql_title_path),
            sql_queries_path=str(sql_queries_path),
            output_dir=str(OUTPUT_DIR),
        )
    except RuntimeError as exc:
        if "cancelled" in str(exc).lower():
            raise HTTPException(status_code=499, detail="Pipeline cancelled.")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Execution failed: {exc}") from exc
    finally:
        with _pipeline_lock:
            _pipeline_running = False
        _pipeline_cancel.clear()


@router.post("/cancel-pipeline")
def cancel_pipeline() -> dict:
    global _pipeline_running
    with _pipeline_lock:
        running = _pipeline_running
    if not running:
        return {"cancelled": False, "message": "No pipeline running."}
    _pipeline_cancel.set()
    return {"cancelled": True, "message": "Cancellation signal sent."}


@router.get("/charts", response_model=ChartListResponse)
def charts() -> ChartListResponse:
    artifacts = list_chart_artifacts()
    return ChartListResponse(charts=artifacts)


@router.get("/charts/{name}")
def chart_by_name(name: str) -> FileResponse:
    try:
        path = get_chart_path(name)
        media_type = "text/html" if path.suffix.lower() == ".html" else "image/png"
        return FileResponse(
            path=str(path),
            media_type=media_type,
            headers={"Content-Disposition": f'inline; filename="{path.name}"'},
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/viewer/{name}", response_class=HTMLResponse)
def chart_viewer(request: Request, name: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "viewer.html",
        {
            "request": request,
            "image_name": name,
            "image_url": f"/output/images/{name}",
        },
    )


@router.post("/generate/report", response_model=ReportGenerationResponse)
def generate_report_endpoint() -> ReportGenerationResponse:
    try:
        df = load_dataset()
        artifacts = list_chart_artifacts()
        report_path = generate_report(df, artifacts)
        return ReportGenerationResponse(
            report_path=str(report_path),
            sections=[
                "Dataset Snapshot",
                "Numeric Summary",
                "Top Category Distributions",
                "Top Correlations",
                "Chart Index",
                "Caveats",
            ],
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Report generation failed: {exc}") from exc


@router.post("/generate/insights", response_model=InsightsGenerationResponse)
def generate_insights_endpoint() -> InsightsGenerationResponse:
    try:
        df = load_dataset()
        artifacts = list_chart_artifacts()
        insights_md_path, insights_html_path, section_paths = generate_insights_bundle(df, artifacts)
        return InsightsGenerationResponse(
            insights_path=str(insights_md_path),
            insights_html_path=str(insights_html_path),
            files_generated=len(section_paths),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Insights generation failed: {exc}") from exc


@router.get("/report", response_model=ReportResponse)
def report() -> ReportResponse:
    try:
        report_path, content = read_report()
        return ReportResponse(report_path=str(report_path), content=content)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/insights", response_model=InsightsResponse)
def insights() -> InsightsResponse:
    try:
        insights_path, content = read_final_insights()
        return InsightsResponse(insights_path=str(insights_path), content=content)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/ask", response_model=AskResponse)
async def ask_question(payload: AskRequest) -> AskResponse:
    import asyncio
    import os

    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=400, detail="OPENROUTER_API_KEY is not set.")

    loop = asyncio.get_event_loop()

    # ── Load SQL queries file directly ────────────────────────────────────────
    sql_dir = SQL_STATUS_PATH.parent
    sql_files = sorted(sql_dir.glob("sql_queries_*.md"))
    if not sql_files:
        raise HTTPException(
            status_code=400,
            detail="No SQL queries file found. Run the pipeline first to generate SQL queries.",
        )
    sql_file = sql_files[-1]
    sql_content = sql_file.read_text(encoding="utf-8").strip()
    context_files: list[str] = [f"output/sql/{sql_file.name}"]

    # ── Extract relevant SQL queries for the sources panel ────────────────────
    def _relevant_sql_queries(catalog_text: str, q: str, max_results: int = 5) -> list[dict[str, str]]:
        """Return up to max_results SQL entries whose title/description matches keywords in q."""
        keywords = {w.lower() for w in re.split(r"\W+", q) if len(w) > 2}
        entries: list[dict[str, str]] = []
        current: dict[str, str] | None = None
        in_sql = False
        sql_lines: list[str] = []
        for line in catalog_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("## ") and not stripped.startswith("### "):
                if current is not None and sql_lines:
                    current["sql"] = "\n".join(sql_lines).strip()
                    title_lower = current.get("title", "").lower()
                    desc_lower = current.get("description", "").lower()
                    if any(kw in title_lower or kw in desc_lower for kw in keywords):
                        entries.append(current)
                current = {"title": stripped[3:].strip(), "description": "", "sql": ""}
                in_sql = False
                sql_lines = []
            elif current is None:
                continue
            elif stripped.startswith("**Description:**"):
                current["description"] = stripped.removeprefix("**Description:**").strip()
            elif stripped == "```sql":
                in_sql = True
                sql_lines = []
            elif stripped == "```" and in_sql:
                in_sql = False
            elif in_sql:
                sql_lines.append(line)
        if current is not None and sql_lines:
            current["sql"] = "\n".join(sql_lines).strip()
            title_lower = current.get("title", "").lower()
            desc_lower = current.get("description", "").lower()
            if any(kw in title_lower or kw in desc_lower for kw in keywords):
                entries.append(current)
        # skip parametric (placeholder) queries — they have no real results
        non_param = [e for e in entries if ":" not in e["sql"]]
        return (non_param or entries)[:max_results]

    sql_queries_for_response = _relevant_sql_queries(sql_content, question)

    # ── Load all individual chart insight files ───────────────────────────────
    insights_dir = OUTPUT_DIR / "insights"
    insights_parts: list[str] = []
    for insight_file in sorted(insights_dir.glob("*.md")):
        if insight_file.name == "insights.md":
            continue  # skip the summary — load individual files for full coverage
        insights_parts.append(insight_file.read_text(encoding="utf-8").strip())
        context_files.append(f"output/insights/{insight_file.name}")
    insights_content = "\n\n---\n\n".join(insights_parts)

    # ── Load statistical report as additional context ─────────────────────────
    report_md_path = OUTPUT_DIR / "report.md"
    report_content = ""
    if report_md_path.exists():
        report_content = report_md_path.read_text(encoding="utf-8").strip()
        context_files.append("output/report.md")

    system_prompt = (
        "You are a data analysis assistant. "
        "Answer strictly based on the provided SQL query results, dataset report, and insights. "
        "Be precise: quote exact values from the data and cite which SQL query or report section supports each claim. "
        "Structure your answer clearly — use bullet points or a short table when comparing multiple values. "
        "If the context does not contain enough information to answer the question, respond with exactly: "
        "'I am unable to answer this question based on the available data.' "
        "Do not fabricate data, statistics, or conclusions beyond what is stated in the context."
    )
    context_block = f"SQL Query Results:\n{sql_content}"
    if report_content:
        context_block += f"\n\n---\n\nDataset Report:\n{report_content}"
    if insights_content:
        context_block += f"\n\n---\n\nInsights:\n{insights_content}"
    user_message = f"{context_block}\n\nQuestion: {question}"

    def _call() -> str:
        import httpx

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        body = {
            "model": OBJECTIVES_MODEL,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        resp = httpx.post(
            f"{OPENROUTER_BASE_URL}/v1/messages",
            json=body,
            headers=headers,
            timeout=60.0,
        )
        data = resp.json()
        if not resp.is_success or data.get("type") == "error":
            err = data.get("error", {})
            raise ValueError(f"OpenRouter error {resp.status_code}: {err.get('message', data)}")
        content = data.get("content")
        if not content:
            raise ValueError(f"Model returned no content. Full response: {data}")
        return next((b["text"] for b in content if b.get("type") == "text"), "")

    try:
        answer = await loop.run_in_executor(None, _call)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"AI request failed: {exc}") from exc

    if "unable to answer" in answer.lower():
        _unanswered_path = SQL_STATUS_PATH.parent / "unanswered_questions.md"
        try:
            existing = _unanswered_path.read_text(encoding="utf-8") if _unanswered_path.exists() else "# Unanswered Questions\n"
            import datetime as _dt
            timestamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            existing += f"\n- [{timestamp}] {question}"
            _unanswered_path.write_text(existing, encoding="utf-8")
        except Exception:
            pass  # never block the response over a logging failure

    return AskResponse(question=question, answer=answer, model_used=OBJECTIVES_MODEL, context_files=context_files, sql_queries=sql_queries_for_response)


@router.get("/gallery", response_class=HTMLResponse)
def gallery(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "gallery.html",
        {"request": request, "charts": [], "images": [], "insights_model": INSIGHTS_MODEL, "objectives_model": OBJECTIVES_MODEL},
    )
