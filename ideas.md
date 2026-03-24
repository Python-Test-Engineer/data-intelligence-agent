Analyse this dataset for biomencial insights using current research best paractices# ideas.md

## Objective
Build a FastAPI-first biomedical analytics service that reads a single dataset (`data/data.csv`), generates reproducible Plotly artifacts, and exposes API endpoints for summary, charts, and report output.

## Core Product Ideas
- Keep architecture service-oriented:
- Routes only orchestrate requests/responses.
- Business logic stays in `src/biomed_api/services/`.
- Schemas remain in `src/biomed_api/models/schemas.py`.
- Use stable output conventions:
- Write generated artifacts only to `output/`.
- Produce HTML charts by default; PNG optional when available.
- Produce `output/report.md` as the standard report artifact.
- Make data handling robust:
- Normalize columns to safe `snake_case`.
- Coerce numeric/date types where valid.
- Never mutate source data on disk.
- Handle missing/malformed data with clear errors.
- Support biomedical-focused insights:
- Clinical distributions and risk comparisons.
- Biomarker summaries and correlation heatmap.
- Survival-style stratifications (risk, MYCN, biomarker median splits).
- Keep interpretation non-causal and research-oriented.

## API Shape (v1)
- `GET /health`
- `GET /summary`
- `POST /generate/charts`
- `GET /charts`
- `GET /charts/{name}`
- `POST /generate/report`
- `GET /report`

## Delivery Principles
- Reset/replace stale implementation in `src/` and `tests/` to align with the FastAPI-first layout.
- Clear stale generated output before regeneration while preserving placeholders like `.gitkeep`.
- Keep defaults explicit and documented so open product decisions can be changed later with minimal refactor.


I want a front end page that accepts a csv to upload into the data folder as data.csv - overwriting existing one - and then implements a plan.md based on these ideas, and then implkements a spce.md a techincal specification of the plan and then executes it.

It then create a plotly dasboard of all the charts and plots that have been created and saved in output/images