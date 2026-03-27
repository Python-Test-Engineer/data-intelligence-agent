from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class ColumnProfile(BaseModel):
    name: str
    dtype: str
    missing_count: int
    missing_pct: float


class SummaryResponse(BaseModel):
    row_count: int
    column_count: int
    missing_cells: int
    missing_pct: float
    columns: list[ColumnProfile]
    key_distributions: dict[str, dict[str, int]]
    description: str = ""


class ChartArtifact(BaseModel):
    name: str
    category: str
    format: str
    path: str


class ChartListResponse(BaseModel):
    charts: list[ChartArtifact]


class ChartGenerationRequest(BaseModel):
    clean_output: bool = Field(default=True)
    write_png: bool = Field(default=True)


class ChartGenerationResponse(BaseModel):
    charts_generated: int
    output_dir: str
    charts: list[ChartArtifact]


class ReportGenerationResponse(BaseModel):
    report_path: str
    sections: list[str]


class ReportResponse(BaseModel):
    report_path: str
    content: str


class InsightsGenerationResponse(BaseModel):
    insights_path: str
    insights_html_path: str
    files_generated: int


class InsightsResponse(BaseModel):
    insights_path: str
    content: str


class CsvUploadResponse(BaseModel):
    message: str
    dataset_path: str
    row_count: int
    column_count: int
    missing_cells: int = 0
    missing_pct: float = 0.0
    description: str = ""


class ExecutePlanRequest(BaseModel):
    clean_output: bool = Field(default=True)
    write_png: bool = Field(default=True)


class ExecutePlanResponse(BaseModel):
    message: str
    charts_generated: int
    html_charts: int
    png_charts: int
    report_path: str
    insights_path: str
    insights_html_path: str
    sql_title_path: str
    sql_queries_path: str
    output_dir: str


class ObjectivesUploadRequest(BaseModel):
    content: str


class ObjectivesUploadResponse(BaseModel):
    message: str
    path: str


class ObjectivesResponse(BaseModel):
    content: str
    path: str


class ResponseToObjectivesResponse(BaseModel):
    message: str
    path: str
    html_path: str
    objectives_found: int
    model_used: str


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    answer: str
    model_used: str
    context_files: list[str] = []


class SqlStatusResponse(BaseModel):
    status: str  # "not_started" | "running" | "ready" | "error"
    message: str = ""
    query_count: int = 0
    original_filename: str = ""


class ErrorResponse(BaseModel):
    detail: str
