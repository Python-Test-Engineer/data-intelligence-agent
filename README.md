# Data Intelligence Agent

A Claude Code–powered data intelligence environment built around a FastAPI CSV analysis service.
Upload any CSV and get automated charts, statistical reports, AI-generated insights, and a
searchable SQL query library — all driven by slash commands and autonomous agents.

---

## LLM Setup

The AI features (`/generate/insights`, `/generate/response-to-objectives`, `/ask`) require an
LLM API key. The default provider is **OpenRouter**, which gives access to hundreds of models
from a single key.

### Option 1 — OpenRouter (default)

1. Sign up at [openrouter.ai](https://openrouter.ai) and create an API key.
2. Copy `.env.example` to `.env` (or create `.env` in the project root) and add:

```env
OPENROUTER_API_KEY=sk-or-...

# Optional: override which model is used for each feature
OPENROUTER_INSIGHTS_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_OBJECTIVES_MODEL=minimax/minimax-m2.5:free
```

The `OPENROUTER_MODEL` variable acts as a fallback for both if the specific vars are not set.
Model IDs use OpenRouter's `provider/model-name` format — browse the full list at
[openrouter.ai/models](https://openrouter.ai/models).

### Option 2 — OpenAI directly

The two LLM services (`insight_service.py`, `objectives_service.py`) use the `anthropic` Python
SDK with a custom `base_url` pointing at OpenRouter. To switch to OpenAI:

**Step 1 — Install the OpenAI SDK:**

```bash
uv add openai
```

**Step 2 — Replace the client in each service.**

In `src/csv_analyser/services/insight_service.py` and
`src/csv_analyser/services/objectives_service.py`, replace the `anthropic` import and client
construction with the OpenAI equivalent:

```python
# Before (OpenRouter via anthropic SDK)
import anthropic
client = anthropic.Anthropic(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api",
)
response = client.messages.create(model="anthropic/claude-4.5-sonnet", ...)

# After (OpenAI)
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(model="gpt-4o", ...)
```

The response shape differs between the two SDKs — `anthropic` returns `response.content[0].text`
while `openai` returns `response.choices[0].message.content`. Update those access patterns in
the same files after swapping the client.

**Step 3 — Set your `.env`:**

```env
OPENAI_API_KEY=sk-...
```

---

## Quick Start

```bash
uv sync
uv run uvicorn csv_analyser.main:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- Gallery:  `http://127.0.0.1:8000/`

---

## CSV Analyser — FastAPI Service

### Architecture

```
src/csv_analyser/
├── main.py                   app bootstrap, lifespan hooks, CORS, structured logging
├── config.py                 PROJECT_ROOT, DATA_PATH, OUTPUT_DIR — single source of truth
├── api/routes.py             all endpoints
├── models/schemas.py         Pydantic request/response models
├── services/
│   ├── data_service.py       CSV loading, type coercion, domain detection
│   ├── chart_service.py      Plotly chart generation (6 chart families, smart time period)
│   ├── dirty_service.py      data quality detection (nulls, dupes, outliers, negatives)
│   ├── report_service.py     statistical summary report
│   ├── insight_service.py    LLM-powered per-chart insights (OpenRouter, streaming)
│   ├── objectives_service.py LLM response to user-defined objectives (streaming + cancellable)
│   └── sql_service.py        in-memory SQLite query execution against uploaded CSV
├── utils/
│   └── html.py               shared markdown-to-HTML renderer (tables, bold, italic, code)
└── templates/
    ├── gallery.html
    └── viewer.html
```

### Analysis Pipeline

```
POST /upload/csv
    └─► data_service   — normalise columns, coerce types, detect domain
    └─► sql_service    — builds SQL catalog in background (automatic, no LLM needed)
POST /generate/charts
    └─► chart_service  — distributions, correlations, time series, scatter
POST /generate/report
    └─► report_service — numeric summary, top categories, correlations, chart index
POST /generate/insights
    └─► insight_service — per-chart AI commentary → insights.md + insights.html
POST /generate/response-to-objectives
    └─► objectives_service — detailed analytical response to OBJECTIVES.md (streaming)
                             (uses SQL catalog + insights as primary context)
POST /ask
    └─► OpenRouter — context-aware Q&A grounded in SQL results + insights
                     supports optional conversation history (last 5 exchanges)
POST /execute
    └─► runs charts + report + insights in one call (cancellable via POST /cancel-pipeline)
        └─► writes GET /pipeline-status step progress throughout
```

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Gallery page |
| GET | `/health` | Health check |
| POST | `/upload/csv` | Upload + validate dataset (50 MB limit, content-type check); triggers SQL catalog build |
| GET | `/summary` | Dataset profile (schema, missingness, domain) |
| GET | `/preview?rows=N` | First N rows of the uploaded dataset as JSON (default 10, max 100) |
| POST | `/generate/charts` | Generate chart bundle (PNG + metadata) |
| GET | `/charts` | List chart artifacts |
| GET | `/charts/{name}` | Fetch chart image |
| GET | `/output-images` | Gallery image cards |
| POST | `/generate/report` | Generate `output/report.md` |
| GET | `/report` | Read generated report |
| POST | `/generate/insights` | Generate per-chart insights + merged HTML |
| GET | `/insights` | Read merged insights |
| POST | `/upload/objectives` | Save `OBJECTIVES.md` content |
| GET | `/objectives` | Read current objectives |
| POST | `/generate/response-to-objectives` | Generate `output/RESPONSE_TO_OBJECTIVES.md` (streaming, cancellable) |
| GET | `/response-to-objectives/download` | Download objectives response (Markdown) |
| GET | `/response-to-objectives/download-html` | Download objectives response (HTML) |
| POST | `/ask` | Ask a question grounded in SQL results + insights; supports `history` for follow-up questions |
| POST | `/execute` | Run full charts + report + insights pipeline (cancellable) |
| POST | `/cancel-pipeline` | Cancel a running `/execute` pipeline (~100–300 ms latency) |
| GET | `/pipeline-status` | Step-level progress during a running pipeline (`step`, `step_index`, `total_steps`) |
| GET | `/sql-status` | Poll SQL catalog build status — returns `status`, `query_count`, `original_filename` |
| POST | `/rerun-sql-catalog` | Re-trigger SQL catalog build for the current CSV |
| GET | `/unanswered-questions` | Questions the AI couldn't answer (logged to `output/sql/unanswered_questions.md`) |
| GET | `/viewer/{name}` | Single-chart viewer page |
| GET | `/gallery` | Full-page chart gallery |

### Output Lifecycle

On every API startup the app resets transient outputs:

- `output/images/` — emptied
- `output/insights/` — emptied
- `output/report.md` — removed
- `output/dirty.csv` — removed
- `output/dirty_rows.md` — removed
- `output/RESPONSE_TO_OBJECTIVES.md` — removed
- `output/RESPONSE_TO_OBJECTIVES.html` — removed

On every CSV upload `output/sql/.status.json` is removed so the gallery UI shows
"not started" for the new dataset, then immediately recreated as `{"status": "running"}`
by the background SQL build task.

Files under `output/sql/` are **not** reset on startup — they are durable artifacts
produced by the SQL commands. They are also protected during pipeline runs: `chart_service.py`
uses `_CLEAN_SKIP = {"sql"}` to prevent `rglob` from deleting any file whose path contains
`sql/`.

### Pipeline Cancellation

`POST /cancel-pipeline` sets a `threading.Event` checked between every pipeline step and
between every LLM token chunk, giving ~100–300 ms cancellation latency. The pipeline returns
HTTP 499 when cancelled. The gallery UI shows a **Cancel** button while a pipeline run is
active and re-enables the **Ask AI** button only after a run completes successfully.

`POST /generate/response-to-objectives` now also streams token-by-token and accepts a
`cancel_event`, matching the same pattern as insight generation.

### Environment Variables

| Variable | Required for | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | `/generate/insights`, `/generate/response-to-objectives`, `/ask` | — |
| `OPENROUTER_INSIGHTS_MODEL` | Model used for per-chart insights | `anthropic/claude-3.5-sonnet` |
| `OPENROUTER_OBJECTIVES_MODEL` | Model used for response-to-objectives | `minimax/minimax-m2.5:free` |
| `OPENROUTER_MODEL` | Fallback model for both services if specific var not set | — |
| `CORS_ORIGINS` | Comma-separated list of allowed origins for CORS | `http://localhost:8000,http://localhost:8001` |
| `LOG_LEVEL` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO` |

A warning is logged at startup if `OPENROUTER_API_KEY` is not set.

---

## What's New (from RECOMMENDATIONS.md)

### Code Quality

- **Removed `_safe_category_from_name` duplication** — the copy in `routes.py` was deleted; both files now import from `chart_service`.
- **Shared markdown-to-HTML renderer** — extracted to `utils/html.py`. Both `insight_service` and `objectives_service` import `render_markdown_to_html` from there. The richer implementation (tables, inline bold/italic/code, horizontal rules) is now used everywhere.
- **`asyncio.get_event_loop()` replaced** — both usages in `routes.py` now call `asyncio.get_running_loop()`, which is safe inside async handlers in Python 3.10+.
- **Inline imports moved to module level** — `asyncio`, `os`, `httpx`, `datetime` are now top-level imports in `routes.py`. Download endpoint imports for `RESPONSE_PATH` / `RESPONSE_HTML_PATH` are also moved to the top.
- **Chart failures now logged** — silent `except: pass` replaced with `logger.warning("Chart %s failed to render: %s", name, exc)`.

### Architecture

- **Anchored path constants** — `config.py` provides `PROJECT_ROOT`, `DATA_PATH`, and `OUTPUT_DIR` anchored to the file's resolved location. All services import from there instead of using `Path("output")` relative strings.
- **Structured logging** — every service has `logger = logging.getLogger(__name__)`. `main.py` configures `basicConfig` with level controlled by the `LOG_LEVEL` env var.
- **`generate_response_to_objectives` is now streaming** — converted from a blocking `client.messages.create()` call to `client.messages.stream()` with a per-chunk `cancel_event` check, matching the pattern in `insight_service`.
- **Per-service model env vars** — `OPENROUTER_INSIGHTS_MODEL` and `OPENROUTER_OBJECTIVES_MODEL` allow independent model selection without touching source code.
- **Startup API key warning** — `main.py` logs a warning at startup if `OPENROUTER_API_KEY` is absent.

### Security

- **50 MB upload limit** — `POST /upload/csv` raises HTTP 413 if the uploaded file exceeds 50 MB.
- **CSV content validation** — after parsing, the endpoint verifies that the DataFrame has at least one column and one row. Content-type is also checked and rejected if it's not `text/csv`, `application/octet-stream`, or `text/plain`.
- **CORS policy** — `CORSMiddleware` is now configured in `main.py`, with allowed origins controlled by the `CORS_ORIGINS` env var.

### New Endpoints

- **`GET /pipeline-status`** — returns `{ running, step, step_index, total_steps }`. The pipeline writes a `.pipeline_step.json` file between each of its 4 steps (loading → charts → report → insights), allowing the frontend to show granular progress.
- **`GET /preview?rows=N`** — returns the first N rows of the uploaded dataset as a JSON array alongside total row count and column list. Useful to verify data loaded correctly before running the pipeline.
- **`GET /unanswered-questions`** — returns the content and count of questions the AI was unable to answer (stored in `output/sql/unanswered_questions.md`).

### UX Improvements

- **Conversation history in `/ask`** — `AskRequest` now accepts an optional `history: list[ChatMessage]` field. Up to the last 5 exchanges are prepended to the messages array sent to the LLM, enabling follow-up questions.
- **Per-chart download links** — each gallery tile now includes a `↓ Download` link pointing to the PNG with the `download` attribute, allowing direct save from the browser without navigating to `/output/images/`.
- **Smart time-series period** — `chart_service` detects the date range and selects the aggregation period automatically:
  - < 90 days → daily (`D`)
  - 90 days – 2 years → monthly (`M`, was always this before)
  - > 2 years → quarterly (`Q`)

---

## SQL Workflow

The SQL pipeline turns any uploaded CSV into a searchable, executable query library. It
operates in two tiers:

### Tier 1 — Server-side auto-build (always runs, no Claude Code required)

When a CSV is uploaded, `sql_service.py` runs as a FastAPI `BackgroundTask`. It builds a
schema-based query catalog automatically and runs all queries against an in-memory SQLite
database, merging results inline. No LLM key is needed.

```
POST /upload/csv
    └─► sql_service (BackgroundTask)
            ├─► generates output/sql/sql_queries_<table>.md   (SQL + inline results)
            ├─► writes output/sql/original_csv.md             (original upload filename)
            └─► writes output/sql/.status.json                (polled by GET /sql-status)
```

The catalog includes **multi-metric analysis** queries automatically generated from the
dataset schema:

- **Performance breakdown by category** — transaction count + all sum/avg metrics grouped by each categorical column
- **Cross-category matrix** — `cat0 × cat1` performance matrix ordered by the best profit/revenue column
- **Unique ID concentration** — distinct ID counts per category to reveal customer or product concentration
- **Monthly trend by category** — `strftime('%Y-%m', date)` breakdown per category to expose seasonal patterns

`GET /sql-status` returns a `SqlStatusResponse` object:

```json
{
  "status": "ready",
  "message": "",
  "query_count": 42,
  "original_filename": "sales_data_q1.csv"
}
```

The gallery UI polls this endpoint every 2 seconds after upload and displays a live spinner
→ green badge with query count → error badge.

### Tier 2 — Claude sql-agent (LLM-enhanced, optional)

When Claude Code is active and a CSV upload is detected, the `sql-agent` runs
`/sql-titles` + `/sql-create` to produce a richer LLM-authored query catalog with
descriptive titles and business-context-aware queries.

```
POST /upload/csv
    └─► sql-agent (if Claude Code session is active)
            ├─► /sql-titles data/<csv>
            │       └─► output/sql/sql_title.md       (LLM-authored titles + descriptions)
            └─► /sql-create output/sql/sql_title.md
                    ├─► output/sql/sql_queries_<table>.md   (SQL + inline test results)
                    └─► output/sql/log_test_at_sql_queries_<table>.md
```

Each entry in the query file is structured for instant Grep retrieval:

```markdown
## Total Revenue by Product
**ARGS:** —
**Description:** Ranks each product by total revenue generated, highest first.
```sql
SELECT product_name,
       SUM(total_revenue) AS total_revenue
FROM sales_data_100
GROUP BY product_name
ORDER BY total_revenue DESC
```
---
```

---

## Claude Code Commands

### SQL Analysis

| Command | Arguments | Output |
|---|---|---|
| `/sql-titles` | `<csv_file>` | `output/sql/sql_title.md` — query titles with descriptions |
| `/sql-create` | `<sql_title.md> [output_file]` | `output/sql/sql_queries_<table>.md` — full SQL catalog |

### Research Pipeline

| Command | Arguments | Output |
|---|---|---|
| `/planner` | `_ideas/<file>.md` | `_plans/<file>.md` — structured research plan |
| `/spec` | `_plans/<file>.md` | `_specs/<file>.md` — Python technical spec |
| `/execute` | `_specs/<file>.md` | Runs all scripts defined in the spec |
| `/insights` | `<image_folder>` | Per-chart insight files + `insights.md` + `insights.html` |
| `/solve` | `<output_folder> <question>` | Evidence-grounded answer from charts and reports |
| `/dashboard` | `<output_folder>` | Interactive Shiny dashboard |

### Developer Utilities

| Command | Purpose |
|---|---|
| `/uv` | `uv sync` and activate the virtual environment |
| `/commit-message` | Draft a commit message from the current git diff |
| `/show-convo` | Show conversation history |
| `/rsi` | Recursive self-improvement — improve commands/skills/agents |
| `/style` | Select an output style for the conversation |

---

## Agents

| Agent | Trigger | Role |
|---|---|---|
| `sql-agent` | When Claude Code is active and a CSV is uploaded | LLM-enhanced SQL catalog: runs `/sql-titles` → `/sql-create` with business-context queries (supplements the server-side auto-build) |
| `data-cleaner` | Before analysis | Scans dataset for dirty rows: nulls, duplicates, outliers |
| `statistician` | After cleaning | Per-column mean/std, top-performing column, plain-English summary |
| `visualizer` | After statistics | Chart titles and one-sentence visual insights |
| `reporter` | After all agents | Assembles final investigation report in Markdown |
| `code-quality-reviewer` | After `/execute` or on request | Reviews code diff for quality and correctness |

---

## Project Structure

```
src/
  csv_analyser/
    config.py                  anchored path constants (PROJECT_ROOT, DATA_PATH, OUTPUT_DIR)
    utils/html.py              shared markdown-to-HTML renderer
    api/routes.py              all HTTP endpoints
    services/                  data, chart, dirty, report, insight, objectives, sql services
    templates/                 gallery.html, viewer.html
data/                          source CSV datasets
output/
  images/                      generated charts (reset on upload)
  insights/                    insight files    (reset on upload)
  sql/                         SQL query library (durable — not reset)
    sql_title.md
    sql_queries_<table>.md
    original_csv.md            original upload filename (persists across resets)
    .status.json               build status polled by GET /sql-status
    unanswered_questions.md    questions the AI could not answer
_ideas/                        research idea files  → /planner input
_plans/                        research plans       → /spec input
_specs/                        technical specs      → /execute input
.claude/
  commands/                    slash command definitions
  agents/                      agent definitions
  output-styles/               output formatting styles
```

---

## Test and Lint

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

### Test Coverage

| Module | Tests |
|---|---|
| `data_service.py` | `tests/test_data_service.py` |
| `chart_service.py` | `tests/test_chart_service.py` |
| `dirty_service.py` | `tests/test_dirty_service.py` — missing values, duplicates, outliers, negatives, non-negative hints |
| `report_service.py` | `tests/test_report_service.py` |
| `insight_service.py` | `tests/test_insight_service.py` |
| `objectives_service.py` | `tests/test_objectives_service.py` — `count_objectives` (bullet/numbered/prose), `render_markdown_to_html` (tables, inline markup) |
| `sql_service.py` | `tests/test_sql_service.py` — catalog generation, SQL code blocks, test execution, inline result merging |
| `api/routes.py` | `tests/test_api_routes.py` |
