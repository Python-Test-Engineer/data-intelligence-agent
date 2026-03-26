from __future__ import annotations

import shutil
from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
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
    SummaryResponse,
)
from csv_analyser.services.chart_service import (
    OUTPUT_DIR,
    generate_standard_charts,
    get_chart_path,
    list_chart_artifacts,
)
from csv_analyser.services.data_service import DATA_PATH, build_summary, load_dataset
from csv_analyser.services.insight_service import MODEL as INSIGHTS_MODEL
from csv_analyser.services.insight_service import generate_insights_bundle, read_final_insights
from csv_analyser.services.objectives_service import MODEL as OBJECTIVES_MODEL
from csv_analyser.services.objectives_service import OPENROUTER_BASE_URL, generate_response_to_objectives
from csv_analyser.services.report_service import generate_report, read_report
from csv_analyser.services.dirty_service import save_dirty_report
from csv_analyser.services.sql_service import generate_sql_catalog


OBJECTIVES_PATH = DATA_PATH.parent.parent / "OBJECTIVES.md"
router = APIRouter()


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


@router.post("/upload/csv", response_model=CsvUploadResponse)
async def upload_csv(file: UploadFile = File(...)) -> CsvUploadResponse:
    try:
        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only .csv files are accepted.")

        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        try:
            pd.read_csv(BytesIO(content))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Malformed CSV: {exc}") from exc

        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_bytes(content)
        _clear_output()

        df = load_dataset(DATA_PATH)
        summary = build_summary(df)
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
        objectives_count = len(
            [
                line
                for line in (
                    OBJECTIVES_PATH.read_text(encoding="utf-8") if OBJECTIVES_PATH.exists() else ""
                ).splitlines()
                if line.strip().startswith("- ") or (line.strip() and line.strip()[0].isdigit())
            ]
        )
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
        generate_sql_catalog(df)
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
    try:
        df = load_dataset()
        artifacts = generate_standard_charts(
            df,
            clean_output=payload.clean_output,
            write_png=payload.write_png,
        )
        save_dirty_report(df)
        report_path = generate_report(df, artifacts)
        insights_md_path, insights_html_path, _ = generate_insights_bundle(df, artifacts)
        sql_title_path, sql_queries_path = generate_sql_catalog(df)
        html_count = sum(1 for artifact in artifacts if artifact.format == "html")
        png_count = sum(1 for artifact in artifacts if artifact.format == "png")
        return ExecutePlanResponse(
            message="Pipeline execution completed. Charts, report, insights, and SQL catalog were generated.",
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
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Execution failed: {exc}") from exc


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

    def _annotate(file_path: Path) -> str:
        """Return file content with every line prefixed by its 1-based line number."""
        lines = file_path.read_text(encoding="utf-8").splitlines()
        return "\n".join(f"L{i + 1}: {line}" for i, line in enumerate(lines))

    context_parts: list[str] = []

    # 1. SQL query catalog — highest priority; never send raw CSV data
    sql_dir = OUTPUT_DIR / "sql"
    if sql_dir.exists():
        for sql_file in sorted(sql_dir.glob("sql_queries_*.md")):
            try:
                context_parts.append(f"FILE: {sql_file.name}\n{_annotate(sql_file)}")
            except Exception:
                pass

    # 2. Chart insights — summarised observations from generated plots
    try:
        insights_path, _ = read_final_insights()
        context_parts.append(f"FILE: {Path(insights_path).name}\n{_annotate(Path(insights_path))}")
    except FileNotFoundError:
        pass

    if not context_parts:
        raise HTTPException(
            status_code=400,
            detail=(
                "No SQL queries or chart insights found. "
                "Please run the pipeline (sections 1–4) and generate SQL queries first."
            ),
        )

    context_block = "\n\n".join(context_parts)

    system_prompt = (
        "You are a data analysis assistant. "
        "You have access to a pre-generated SQL query catalog and chart insights — use these as your sole sources. "
        "Each line in every file is prefixed with its line number (e.g. 'L42: ...'). "
        "When a question can be answered by a SQL query, include the full query in a ```sql block. "
        "When a question relates to visual patterns or trends, use the chart insights. "
        "Do not fabricate data, statistics, or conclusions beyond what is stated in the context. "
        "Never request or use raw CSV data. "
        "If the context is insufficient to answer the question, say so clearly. "
        "ALWAYS end your answer with a '### Sources' section listing each source as: "
        "`- <filename>:<line-range> — <query title or insight heading>`"
    )
    user_message = f"Context:\n{context_block}\n\nQuestion: {question}"

    def _call() -> str:
        import httpx

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        body = {
            "model": OBJECTIVES_MODEL,
            "max_tokens": 1024,
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
        if not resp.is_success:
            err = data.get("error", {})
            raise ValueError(f"OpenRouter error {resp.status_code}: {err.get('message', data)}")
        content = data.get("content")
        if not content:
            raise ValueError(f"Model returned no content. Full response: {data}")
        return next((b["text"] for b in content if b.get("type") == "text"), "")

    try:
        loop = asyncio.get_event_loop()
        answer = await loop.run_in_executor(None, _call)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"AI request failed: {exc}") from exc

    return AskResponse(question=question, answer=answer, model_used=OBJECTIVES_MODEL)


@router.get("/gallery", response_class=HTMLResponse)
def gallery(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "gallery.html",
        {"request": request, "charts": [], "images": [], "insights_model": INSIGHTS_MODEL, "objectives_model": OBJECTIVES_MODEL},
    )
