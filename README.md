# Biomedical FastAPI App

FastAPI service that reads `data/data.csv`, generates biomedical Plotly charts in `output/`, serves a frontend dashboard, and creates `output/report.md`.

## Architecture

- API routes: `src/biomed_api/api/routes.py`
- Business logic: `src/biomed_api/services/`
- Schemas: `src/biomed_api/models/schemas.py`
- Templates: `src/biomed_api/templates/gallery.html`

## Open Decision Defaults

- Gallery mode: `API + HTML` (`GET /gallery`)
- Chart selection behavior: pre-generated standard bundle with list filtering
- Report outputs: Markdown only (`output/report.md`)
- Output retention: clean overwrite on generation (`clean_output=true` default)

## Environment Variables

No environment variables are required for local execution.

## Run

```bash
uv sync
uv run uvicorn biomed_api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for API docs and `http://127.0.0.1:8000/` for the frontend dashboard.

## Endpoints

- `GET /`
- `GET /health`
- `POST /upload/csv`
- `GET /summary`
- `POST /generate/charts`
- `POST /execute`
- `GET /charts`
- `GET /charts/{name}`
- `POST /generate/report`
- `GET /report`
- `GET /gallery`

## Test and Lint

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```
