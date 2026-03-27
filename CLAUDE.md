# CLAUDE.md — Data Intelligence Agent

## What this project is

A data intelligence environment with two layers:

1. **`src/csv_analyser`** — FastAPI service that ingests any CSV and produces charts,
   statistical reports, AI insights (via OpenRouter), and answers to user-defined objectives.
   This is the primary application.

2. **Claude Code commands** — slash commands that extend the analysis workflow with SQL
   query generation, research planning, and insight synthesis.

`src/biomed_api` mirrors `csv_analyser` in structure but is a secondary module for
biomedical-specific work. Default to `csv_analyser` for all changes unless the user
explicitly mentions `biomed_api`.

## Run the app

```bash
uv run uvicorn csv_analyser.main:app --reload
```

## Key source paths

| What | Where |
|---|---|
| API routes | `src/csv_analyser/api/routes.py` |
| Data loading / type coercion | `src/csv_analyser/services/data_service.py` |
| Chart generation | `src/csv_analyser/services/chart_service.py` |
| Data quality detection | `src/csv_analyser/services/dirty_service.py` |
| AI insight generation | `src/csv_analyser/services/insight_service.py` |
| Objectives response | `src/csv_analyser/services/objectives_service.py` |
| Statistical report | `src/csv_analyser/services/report_service.py` |
| SQL catalog + test execution | `src/csv_analyser/services/sql_service.py` |
| Pydantic schemas | `src/csv_analyser/models/schemas.py` |
| HTML templates | `src/csv_analyser/templates/` |

## Output directories

| Directory | Contents | Reset on startup? |
|---|---|---|
| `output/images/` | Generated chart PNGs | Yes |
| `output/insights/` | Per-chart insight markdown + HTML | Yes |
| `output/sql/` | SQL query catalog (`sql_title.md`, `sql_queries_*.md`, `original_csv.md`) | **No** |
| `data/` | Source CSV files | No |

`output/sql/` is also protected **during pipeline runs**: `chart_service.py` uses
`_CLEAN_SKIP = {"sql"}` so `ensure_output_dir(clean=True)` never touches files whose
path contains `sql/`. Do not remove this guard.

## SQL commands

The SQL workflow is a key part of this project. Always look here first when a user asks
about SQL queries or wants to query a dataset:

- `output/sql/sql_title.md` — catalog of query titles with descriptions
- `output/sql/sql_queries_<table>.md` — executable SQL for every title
- `output/sql/original_csv.md` — the original filename of the last uploaded CSV (persists across pipeline resets)

Retrieve a query: `Grep pattern: "## <Title>"` in the queries file.

## SQL workflow

### Server-side auto-build (always happens)

On every CSV upload, `routes.py` schedules `_build_sql_catalog_bg(csv_path)` as a
FastAPI `BackgroundTask`. This calls `sql_service.generate_sql_catalog()` and
`sql_service.run_tests_and_merge()` — no LLM key required. It writes
`output/sql/.status.json` at start and completion; all states include `original_filename`
(e.g. `{"status": "ready", "original_filename": "sales_data.csv"}`). It also writes
`output/sql/original_csv.md` with the human-readable filename. The gallery UI polls
`GET /sql-status` every 2 s and shows a live status indicator.

### Claude sql-agent (LLM-enhanced, supplementary)

When you are in a Claude Code session and a CSV upload completes, also launch the
`sql-agent` to produce an LLM-authored query catalog with better titles and
business-context-aware queries:

```
Agent tool → subagent_type: sql-agent
```

The agent runs:
1. `/sql-titles data/<csv>` — generates `output/sql/sql_title.md`
2. `/sql-create output/sql/sql_title.md` — generates SQL catalog with inline test results

Do **not** call `/sql-test` via the Skill tool — nested Skill invocations silently fail.
`/sql-create` embeds its own test execution via direct Bash scripts.

### Context usage

Both `/ask` and `/generate/response-to-objectives` load `output/sql/sql_queries_*.md`
as their primary context (SQL results contain exact computed values). `insights.md` is
secondary context. Never load raw CSV data as context.

## Pipeline cancellation

`POST /cancel-pipeline` sets a `threading.Event` that is checked:
- Between every step in `execute_plan`
- Between every token chunk in the streaming LLM calls in `insight_service.py`

This gives ~100–300 ms cancellation latency. The pipeline returns HTTP 499 when cancelled.

## LLM / API keys

- **OpenRouter** (`OPENROUTER_API_KEY`) — used for insights, objectives, and `/ask`
- Core routes (upload, summary, charts, report) work without any key

## Testing and lint

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

Ruff line length: 100. Target: Python 3.11.

## What NOT to do

- Do not touch `src/biomed_api` unless the user explicitly asks
- Do not commit files from `output/images/` or `output/insights/`
- Do not add API keys to source files or tests
- Do not remove `_CLEAN_SKIP = {"sql"}` from `chart_service.py` — it prevents the pipeline from deleting SQL catalog files
- Do not call `/sql-test` via the Skill tool from inside another skill — nested Skill invocations silently fail; use direct Bash scripts instead
- Do not call `generate_sql_catalog()` from inside `execute_plan` or `generate_charts` — the catalog is built on upload; the pipeline should only read existing SQL files
