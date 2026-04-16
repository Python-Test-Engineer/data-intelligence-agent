# AGENTS Guide

Practical working rules for coding agents in this repository.

## Project Snapshot

- **Name:** `data-intelligence-agent`
- **Stack:** Python 3.11+, FastAPI, Plotly, Pandas, Jinja2, OpenRouter
- **Primary package:** `src/csv_analyser`
- **Test suite:** `tests/`
- **Key runtime directories:**
  - `data/` — uploaded CSV files
  - `output/images/` — generated charts (reset on API startup)
  - `output/insights/` — generated insight artifacts (reset on API startup)
  - `output/sql/` — SQL query catalog (durable, not reset)

## Setup and Run

```bash
uv sync
uv run uvicorn csv_analyser.main:app --reload
```

Common checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Code Map

| File | Purpose |
|---|---|
| `src/csv_analyser/main.py` | App bootstrap, lifespan hooks, static file serving |
| `src/csv_analyser/api/routes.py` | All API endpoints |
| `src/csv_analyser/models/schemas.py` | Pydantic request/response models |
| `src/csv_analyser/services/data_service.py` | CSV loading, column normalisation, type coercion, domain detection |
| `src/csv_analyser/services/chart_service.py` | Plotly chart generation (6 chart families) |
| `src/csv_analyser/services/dirty_service.py` | Data quality detection: nulls, duplicates, outliers, semantic violations |
| `src/csv_analyser/services/report_service.py` | Statistical summary report generation |
| `src/csv_analyser/services/insight_service.py` | LLM-powered per-chart insights via OpenRouter |
| `src/csv_analyser/services/objectives_service.py` | LLM response to user-defined objectives |
| `src/csv_analyser/templates/` | Jinja2 HTML templates (gallery, viewer) |

## Output Lifecycle

On API startup, transient outputs are reset by the app lifecycle:

- `output/images/` is emptied
- `output/insights/` is emptied
- `output/report.md` is removed
- `output/RESPONSE_TO_OBJECTIVES.md` is removed

**Do not treat those files as durable state.**

`output/sql/` is **not** reset — it holds the SQL query catalog produced by `/sql-titles`
and `/sql-create` commands and should be preserved across runs.

## Environment Variables

- `OPENROUTER_API_KEY` — required for `/generate/insights`, `/generate/response-to-objectives`, and `/ask`
- Core routes (`/upload/csv`, `/summary`, `/generate/charts`, `/generate/report`) work without any API key

## Protected Files — Never Delete

The following files and directories must **never** be deleted, moved, or overwritten by any agent action, cleanup routine, or pipeline step:

- `_ideas/kaggle_ideas.md`
- `_plans/kaggle_plan.md`
- `_specs/kaggle_specs.md`

These contain research briefs, analysis plans, and technical specs used for presentations and interviews. They are not generated artifacts — they are source documents. If a pipeline or cleanup step would affect these paths, skip them explicitly.

## Agent Working Rules

- Keep changes minimal and scoped to the user request
- Preserve module boundaries: routes call services; services hold business logic
- Add or update tests in `tests/` for any behavior changes
- Do not commit generated artifacts in `output/` unless explicitly requested
- Do not introduce secrets into code, tests, or fixtures
- Keep lint and tests passing for any touched behavior

## Editing Conventions

- Follow Ruff line length (`100`) and Python 3.11 compatibility
- Use explicit, readable function names; avoid ambiguous abbreviations
- Add comments only where logic is non-obvious
- Keep API responses and schema fields consistent with existing route patterns

## Recommended Change Workflow

1. Read impacted route/service/test files
2. Implement focused code changes
3. Run targeted tests first, then broader suite
4. Run `ruff check` (and `ruff format` if required)
5. Summarise behavioral changes and any residual risks
