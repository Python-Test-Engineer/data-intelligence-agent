# Data Intelligence Agent — CLAUDE.md

## Project overview

FastAPI service (`src/csv_analyser`) that accepts a CSV upload and runs an AI-powered analytics pipeline: chart generation (Plotly), a statistical report, per-chart LLM insights, an SQL query catalog, and a Q&A endpoint. The frontend is a Jinja2 gallery at `src/csv_analyser/templates/gallery.html`.

## Start the dev server

```bash
uv run uvicorn csv_analyser.main:app --app-dir src --reload --port 8001
```

App: http://127.0.0.1:8001 · Docs: http://127.0.0.1:8001/docs

## Key paths

| Path | Purpose |
|------|---------|
| `src/csv_analyser/api/routes.py` | All FastAPI routes and pipeline logic |
| `src/csv_analyser/services/` | chart, data, dirty, insight, objectives, report, sql services |
| `src/csv_analyser/config.py` | `PROJECT_ROOT`, `DATA_PATH`, `OUTPUT_DIR` |
| `data/data.csv` | Active dataset (written on upload, read by all services) |
| `output/` | Generated artefacts (images, insights, report, SQL catalog) |
| `OBJECTIVES.md` | User-supplied business questions answered by the pipeline |
| `_ideas/`, `_plans/`, `_specs/` | **Never delete** — used for interview/talk prep |

## Pipeline steps (`POST /execute`)

1. Load dataset → 2. Generate charts → 3. Generate dirty-rows report + statistical report → 4. Generate LLM insights

SQL catalog is built **on upload** as a `BackgroundTask`, not inside `/execute`.

## SQL catalog — two-tier architecture

- **Tier 1 (server):** `_build_sql_catalog_bg` runs on every CSV upload; writes `output/sql/sql_queries_*.md` and updates `output/sql/.status.json`.
- **Tier 2 (Claude Code):** the `sql-agent` skill builds an LLM-enhanced version when Claude Code is active.
- `output/sql/` is protected by a `_CLEAN_SKIP` guard in `chart_service.py` — the pipeline `rglob` never deletes SQL files.

## /ask route context order

Load context in this order: SQL catalog first → per-chart insight files second → report.md third. Never pass raw CSV rows to the LLM.

## Pipeline cancellation

Use `messages.stream()` with a per-chunk `cancel_event` check to achieve ~100–300 ms cancellation latency. The `_pipeline_cancel` threading.Event is set by `POST /cancel-pipeline`.

## Environment

```
OPENROUTER_API_KEY=...   # required for all LLM features
LOG_LEVEL=INFO           # optional
CORS_ORIGINS=...         # comma-separated, defaults to localhost:8000,8001
```

## Skills (Claude Code)

| Skill | When to use |
|-------|------------|
| `/planner` | Turn an `_ideas/` file into a structured research plan |
| `/spec` | Turn a `_plans/` file into a Python technical spec |
| `/execute` | Implement and run scripts from a `_specs/` file |
| `/sql-titles` | Generate SQL query titles from a CSV |
| `/sql-create` | Generate and test SQL from a titles file |
| `/solve` | Answer a question grounded in an `output/` folder |
| `/insights` | Generate a deep insights report from chart images |
| `/dashboard` | Build an interactive Shiny dashboard from output |
| `/uv` | Run `uv sync` and activate the virtual environment |

## Do not

- Delete or overwrite files in `_ideas/`, `_plans/`, `_specs/`
- Call a Skill from inside a running skill (nested invocations silently fail — embed logic as direct Bash instead)
- Remove the `_CLEAN_SKIP` guard in `chart_service.py`
