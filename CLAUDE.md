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
| Pydantic schemas | `src/csv_analyser/models/schemas.py` |
| HTML templates | `src/csv_analyser/templates/` |

## Output directories

| Directory | Contents | Reset on startup? |
|---|---|---|
| `output/images/` | Generated chart PNGs | Yes |
| `output/insights/` | Per-chart insight markdown + HTML | Yes |
| `output/sql/` | SQL query catalog (`sql_title.md`, `sql_queries_*.md`) | **No** |
| `data/` | Source CSV files | No |

## SQL commands

The SQL workflow is a key part of this project. Always look here first when a user asks
about SQL queries or wants to query a dataset:

- `output/sql/sql_title.md` — catalog of query titles with descriptions
- `output/sql/sql_queries_<table>.md` — executable SQL for every title

Retrieve a query: `Grep pattern: "## <Title>"` in the queries file.

## Pipeline workflow — REQUIRED

Whenever the chart pipeline runs (POST `/execute`, POST `/generate/charts`, or any action
that triggers chart generation), you MUST automatically continue with the SQL workflow in
this exact order — **without waiting to be asked**:

1. Run `/sql-titles data/data.csv`
2. Run `/sql-create output/sql/sql_title.md`

Do not skip these steps. Do not ask for confirmation. Run them immediately after charts are
generated.

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
