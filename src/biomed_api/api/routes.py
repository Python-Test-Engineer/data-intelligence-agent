from __future__ import annotations

import shutil
from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from biomed_api.models.schemas import (
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
from biomed_api.services.chart_service import (
    OUTPUT_DIR,
    generate_standard_charts,
    get_chart_path,
    list_chart_artifacts,
)
from biomed_api.services.data_service import DATA_PATH, build_summary, load_dataset
from biomed_api.services.insight_service import MODEL as INSIGHTS_MODEL
from biomed_api.services.insight_service import generate_insights_bundle, read_final_insights
from biomed_api.services.objectives_service import MODEL as OBJECTIVES_MODEL
from biomed_api.services.objectives_service import OPENROUTER_BASE_URL, generate_response_to_objectives
from biomed_api.services.report_service import generate_report, read_report
from biomed_api.services.dirty_service import save_dirty_report


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
    if name.startswith("clinical_"):
        return "clinical"
    if name.startswith("biomarker_"):
        return "biomarker"
    if name.startswith("survival_"):
        return "survival"
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
    from biomed_api.services.objectives_service import RESPONSE_PATH
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
        html_count = sum(1 for artifact in artifacts if artifact.format == "html")
        png_count = sum(1 for artifact in artifacts if artifact.format == "png")
        return ExecutePlanResponse(
            message="Plan/spec execution completed. Charts, report, and insights were generated.",
            charts_generated=len(artifacts),
            html_charts=html_count,
            png_charts=png_count,
            report_path=str(report_path),
            insights_path=str(insights_md_path),
            insights_html_path=str(insights_html_path),
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
                "Cohort Snapshot",
                "Outcome Stratification",
                "Top Biomarker-EFS Associations",
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

    # Require generated insights — do not use raw dataset as context
    try:
        _, insights_content = read_final_insights()
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail=(
                "No insights have been generated yet. "
                "Please run all sections (1–4) first to generate insights before asking questions."
            ),
        )

    # Add chart list as supplementary context
    context_parts: list[str] = [f"Insights:\n{insights_content}"]
    try:
        artifacts = list_chart_artifacts()
        if artifacts:
            chart_names = ", ".join(a.name for a in artifacts)
            context_parts.append(f"Available charts: {chart_names}")
    except Exception:
        pass

    context_block = "\n\n".join(context_parts)

    system_prompt = (
        "You are a biomedical data scientist assistant. "
        "Answer questions strictly based on the provided insights and chart information. "
        "Do not fabricate data, statistics, or conclusions beyond what is stated in the context. "
        "If the context is insufficient to answer the question, say so clearly."
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
