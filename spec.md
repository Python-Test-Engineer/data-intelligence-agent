# FastAPI + Plotly Biomedical App Specification

## Objective
Implement a FastAPI application that ingests `data/data.csv`, generates biomedical charts, exposes a selectable chart gallery, and writes a research findings report to `output/report.md`.

## Mandatory Implementation Reset
- Replace existing application code in `src/` with a FastAPI-first implementation.
- Replace existing tests in `tests/` with FastAPI and service-level tests aligned to the new architecture.
- Remove stale generated artifacts in `output/` before regeneration (preserve only placeholder files like `.gitkeep` if needed).

## Tech Stack
- Python 3.11+
- FastAPI + Uvicorn
- Plotly + Pandas + NumPy
- Jinja2 (if HTML gallery page is included)
- Pytest (+ `httpx`/`starlette` test client for API tests)
- Ruff
- `uv` for dependency and environment management

## Target Project Structure
```text
src/biomed_api/main.py
src/biomed_api/api/routes.py
src/biomed_api/services/data_service.py
src/biomed_api/services/chart_service.py
src/biomed_api/services/report_service.py
src/biomed_api/models/schemas.py
src/biomed_api/templates/gallery.html        # optional if HTML gallery enabled
tests/test_data_service.py
tests/test_chart_service.py
tests/test_report_service.py
tests/test_api_routes.py
output/                                      # generated charts + report
data/data.csv
pyproject.toml
README.md
```

## `uv` Setup and Run Commands
1. `uv sync`
2. `uv run uvicorn biomed_api.main:app --reload`
3. `uv run pytest`
4. `uv run ruff check .`
5. `uv run ruff format .`

## Functional Requirements
- `GET /health`: basic service health.
- `GET /summary`: dataset profile (row count, columns, missingness, key distributions).
- `POST /generate/charts`: generate standard chart bundle into `output/`.
- `GET /charts`: list generated chart artifacts with category metadata.
- `GET /charts/{name}`: return chart file or metadata for selected chart.
- `POST /generate/report`: generate `output/report.md` from current data/stats/charts.
- `GET /report`: fetch report content and path metadata.

## Chart Bundle (v1)
- Clinical: age distribution, stage distribution, risk distribution, EFS by risk.
- Biomarker: marker summary, selected expression scatter plots, expression correlation heatmap.
- Survival-focused: KM-style by risk, KM-style by MYCN, median-split KM-style for top biomarkers, event-rate heatmap.
- Output format: HTML required, PNG optional (when image engine is available).

## Data and Processing Rules
- Read source only from `data/data.csv`.
- Normalize column names to safe snake_case identifiers.
- Coerce numeric/date types where valid; handle parsing failures gracefully.
- Do not mutate source data on disk.
- Ensure missing values never crash chart/report generation.

## Report Requirements
- Write `output/report.md` with:
- Cohort snapshot
- Outcome stratification (risk and MYCN)
- Top biomarker-EFS associations
- Chart index references
- Caveats and non-causal interpretation note

## Testing Requirements
- Data service: load, schema inference, missing-file behavior.
- Chart service: artifacts created in `output/`, expected count/categories.
- Report service: markdown generated with required sections.
- API routes: status codes, response schema, happy path for generation endpoints.

## Acceptance Criteria
- App starts via `uvicorn` command above.
- Full generation flow works end-to-end:
1. `/summary` returns valid dataset profile.
2. `/generate/charts` produces chart artifacts in `output/`.
3. `/charts` lists selectable artifacts.
4. `/generate/report` produces `output/report.md`.
- Tests pass via `uv run pytest`.
- Lint checks pass via `uv run ruff check .`.

## Open Decisions (Must Confirm Before Final Build)
1. Gallery mode: API-only vs API + HTML page.
2. Chart selection behavior: pre-generated filter vs on-demand regeneration.
3. Report outputs: Markdown only vs Markdown + PDF/HTML.
4. Output retention: clean overwrite vs timestamped versioning.
