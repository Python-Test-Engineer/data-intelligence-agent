# plan.md

## Spec: FastAPI Biomedical Analytics Service

### 1. Scope and Required Outcomes
- Implement and maintain the FastAPI-first architecture in `src/biomed_api/`.
- Read input only from `data/data.csv`.
- Expose required API routes:
- `GET /health`
- `GET /summary`
- `POST /generate/charts`
- `GET /charts`
- `GET /charts/{name}`
- `POST /generate/report`
- `GET /report`
- Generate chart/report artifacts into `output/` only.
- Ensure failures for missing/malformed data are explicit and non-crashing.

### 2. Module Responsibilities
- `api/routes.py`: request validation, response shaping, error translation.
- `services/data_service.py`: load dataset, normalize columns, infer types, summary and missingness profile.
- `services/chart_service.py`: build biomedical chart bundle and persist artifacts.
- `services/report_service.py`: render `output/report.md` with required sections.
- `models/schemas.py`: Pydantic contracts for summary and generation endpoints.
- `templates/gallery.html`: chart gallery rendering for generated artifacts.

### 3. Data Processing Rules
- Convert column names to safe `snake_case`.
- Coerce numeric/date types where valid without destructive conversion.
- Preserve source CSV unchanged on disk.
- Guard all processing against null-heavy columns and malformed values.

### 4. Chart Bundle Spec (v1)
- Clinical distributions and risk comparisons.
- Biomarker summaries.
- Correlation heatmap for numeric biomarkers.
- Survival-style stratifications by:
- risk group
- MYCN status (or closest available field)
- biomarker median split cohorts
- Output format:
- HTML required.
- PNG optional when available.

### 5. Report Spec
- Write `output/report.md`.
- Include:
- cohort snapshot
- outcome stratification
- biomarker vs EFS associations
- chart index
- caveats
- Language must remain non-causal and research-oriented.

### 6. Reset/Regeneration Rules
- Replace stale app code under `src/` with the FastAPI-first module layout.
- Replace stale tests under `tests/` to reflect route/service behavior.
- Clear stale generated artifacts from `output/` before regeneration.
- Preserve placeholders such as `.gitkeep`.

### 7. Test Acceptance Criteria
- `tests/test_data_service.py`:
- dataset load success
- inferred schema summary shape
- missing-file error behavior
- `tests/test_chart_service.py`:
- chart artifacts created
- expected category/count checks
- `tests/test_report_service.py`:
- required markdown sections present
- `tests/test_api_routes.py`:
- status code coverage
- response schema checks
- generation happy paths

### 8. Runbook
1. `uv sync`
2. `uv run uvicorn biomed_api.main:app --reload`
3. `uv run pytest`
4. `uv run ruff check .`
5. `uv run ruff format .` (if formatting is needed)

### 9. Default Product Decisions
- Gallery mode: include both API listing and HTML gallery page.
- Chart generation: pre-generate standard bundle on request, list from stored artifacts.
- Report format: Markdown only (`output/report.md`) in v1.
- Output retention: replace previous generated artifacts on each regeneration run.
