from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from biomed_api.models.schemas import (
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

OBJECTIVES_PATH = DATA_PATH.parent.parent / "OBJECTIVES.md"
from biomed_api.services.insight_service import generate_insights_bundle, read_final_insights
from biomed_api.services.objectives_service import generate_response_to_objectives
from biomed_api.services.report_service import generate_report, read_report


router = APIRouter()
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
        {"request": request, "charts": [], "images": []},
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

        df = load_dataset(DATA_PATH)
        return CsvUploadResponse(
            message="CSV uploaded successfully and saved as data/data.csv.",
            dataset_path=str(DATA_PATH),
            row_count=len(df),
            column_count=len(df.columns),
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
        out_path = await loop.run_in_executor(None, generate_response_to_objectives, artifacts)
        objectives_count = len(
            [l for l in (OBJECTIVES_PATH.read_text(encoding="utf-8") if OBJECTIVES_PATH.exists() else "").splitlines()
             if l.strip().startswith("- ") or (l.strip() and l.strip()[0].isdigit())]
        )
        return ResponseToObjectivesResponse(
            message="RESPONSE_TO_OBJECTIVES.md generated successfully.",
            path=str(out_path),
            objectives_found=objectives_count,
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
    try:
        path = get_chart_path(name)
        return templates.TemplateResponse(
            request,
            "viewer.html",
            {
                "request": request,
                "image_name": path.name,
                "image_url": f"/charts/{path.name}",
            },
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


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


@router.get("/gallery", response_class=HTMLResponse)
def gallery(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "gallery.html",
        {"request": request, "charts": [], "images": []},
    )
