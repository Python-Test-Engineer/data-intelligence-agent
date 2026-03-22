# Repository Guidelines

When making Plotly ensure images are saved as images not just as html files with images.

## Project Structure & Module Organization
This repository targets a FastAPI + Plotly biomedical analytics service.

Use this layout:

```text
src/biomed_api/main.py
src/biomed_api/api/routes.py
src/biomed_api/services/data_service.py
src/biomed_api/services/chart_service.py
src/biomed_api/services/report_service.py
src/biomed_api/models/schemas.py
src/biomed_api/templates/gallery.html
tests/test_data_service.py
tests/test_chart_service.py
tests/test_report_service.py
tests/test_api_routes.py
data/data.csv
output/
```

Guidelines:
- Keep HTTP route definitions in `api/routes.py` and business logic in `services/`.
- Keep schema contracts in `models/schemas.py`.
- Treat `data/data.csv` as the single source input.
- Generated artifacts belong in `output/` only.

## Mandatory Reset Rules
When implementing against the current plan/spec:
- Replace existing app code in `src/` with the FastAPI-first architecture.
- Replace existing tests in `tests/` to match new API/service behavior.
- Clear stale generated artifacts in `output/` before regeneration.
- Preserve placeholders like `.gitkeep` where needed.

## Build, Test, and Development Commands
Use `uv` for dependency management and execution.

- `uv sync`
- `uv run uvicorn biomed_api.main:app --reload`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format .`

Dependency additions:
- Runtime: `uv add <package>`
- Dev: `uv add --dev <package>`

## Coding Style & Naming Conventions
- Python: 4-space indentation, explicit type hints on public functions.
- Naming: `snake_case` for modules/functions/variables, `PascalCase` for classes.
- Keep services small and testable; avoid route handlers with heavy logic.
- Use Ruff for linting/formatting.

## Functional API Requirements
Minimum endpoints:
- `GET /health`
- `GET /summary`
- `POST /generate/charts`
- `GET /charts`
- `GET /charts/{name}`
- `POST /generate/report`
- `GET /report`

Behavior requirements:
- `/summary` returns row/column profile and missingness.
- Chart/report generation must fail with clear errors, not unhandled exceptions.
- Missing or malformed data should be handled gracefully.

## Biomedical Data, Charts, and Report Rules
Data processing:
- Normalize columns to safe `snake_case`.
- Coerce numeric/date types where valid.
- Do not mutate source data on disk.
- Ensure missing values never crash chart or report generation.

v1 chart bundle expectations:
- Clinical distributions and risk comparisons.
- Biomarker summaries and correlation heatmap.
- Survival-style stratifications (risk, MYCN, biomarker median splits).
- Save chart outputs to `output/` as HTML (PNG optional).

Report expectations:
- Generate `output/report.md`.
- Include cohort snapshot, outcome stratification, biomarker-EFS associations, chart index, and caveats.
- Keep interpretation non-causal and research-oriented.

## Testing Guidelines
- Keep tests under `tests/` and mirror service/API modules.
- Required coverage:
- Data service: load, schema inference, missing-file behavior.
- Chart service: artifact creation and expected category/count checks.
- Report service: required markdown sections written.
- API routes: status codes, schema shape, and generation happy paths.
- Run `uv run pytest` before PR submission.

## Commit & Pull Request Guidelines
Use short, imperative commit messages, for example:
- `Implement FastAPI chart generation endpoints`
- `Add report service markdown section checks`

PRs should include:
- Concise summary of behavior changes.
- Test/lint evidence (`uv run pytest`, `uv run ruff check .`).
- Linked issue/task ID when applicable.
- API samples or screenshots for gallery/UI changes.

## Open Decisions Handling
If unresolved product choices remain (gallery mode, chart selection behavior, report formats, output retention):
- Use explicit defaults in code.
- Document defaults in `README.md` and API docs.
- Keep implementation structured so these can be switched later with minimal refactor.

## Configuration & Security Notes
- Never commit secrets, API keys, or machine-specific config.
- Keep local config in ignored files (for example `.env`).
- Document required environment variables in `README.md`.
