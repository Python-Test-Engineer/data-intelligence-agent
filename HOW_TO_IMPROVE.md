# How to Improve the Data Intelligence Agent

This guide covers the concrete levers available to increase the capability, accuracy, and performance of this agent — ordered from highest to lowest impact.

---

## 1. Model Selection (Highest Impact)

The single most effective improvement is choosing stronger LLM models. Model selection is controlled entirely through environment variables in your `.env` file.

### Chart Insights

```env
OPENROUTER_INSIGHTS_MODEL=anthropic/claude-sonnet-4-5
```

This model analyses every chart image and produces the `data_insight`, `analysis_insight`, and `caveat` fields. Upgrading to a more capable model directly improves the quality of every insight on your dashboard.

| Model | Quality | Speed | Cost |
|---|---|---|---|
| `anthropic/claude-haiku-4-5` | Good | Fastest | Cheapest |
| `anthropic/claude-sonnet-4-5` | Great *(recommended)* | Medium | Medium |
| `anthropic/claude-opus-4-6` | Best | Slowest | Most expensive |
| `openai/gpt-4.1` | Great | Fast | Medium |
| `openai/gpt-4.1-mini` | Good | Fastest | Cheapest |
| `google/gemini-2.5-pro` | Great | Medium | Medium |
| `google/gemini-2.0-flash` | Good | Fast | Low |

> Check [openrouter.ai/models](https://openrouter.ai/models) for the latest available models and pricing.

### Objectives Response

```env
OPENROUTER_OBJECTIVES_MODEL=minimax/minimax-m2.5:free
```

This model reads your `OBJECTIVES.md` and answers each objective using the full SQL catalog, report, and insights as context. The default (`minimax-m2.5:free`) is a free model — upgrading it has a large effect on response quality.

**Recommended upgrade:**

```env
OPENROUTER_OBJECTIVES_MODEL=anthropic/claude-sonnet-4-5
```

### Fallback for Both

```env
OPENROUTER_MODEL=anthropic/claude-sonnet-4-5
```

If neither of the specific model vars is set, both services fall back to this value.

---

## 2. Use the Enhanced SQL Catalog (Tier 2)

The agent builds a basic SQL catalog automatically when you upload a CSV. This covers generic aggregations but has no knowledge of your specific business context.

Running the Claude Code SQL workflow generates 80–100 domain-aware queries with real test results baked in. This significantly improves the `/ask` (Ask AI) feature because it has richer, pre-executed context to draw from.

**Step 1 — Generate query titles:**

```
/sql-titles
```

This inspects your CSV and produces categorised query titles tailored to your dataset's columns and apparent domain.

**Step 2 — Generate full SQL with test results:**

```
/sql-create output/sql/sql_title.md
```

This writes SQL for every title, runs each query against your actual data in SQLite, and embeds the results inline. The Ask AI feature then uses this tested catalog as its primary evidence source.

**Why this matters:** Ask AI matches your question to the 5 most relevant queries. A richer catalog means more relevant matches and more accurate answers.

---

## 3. Write a Detailed OBJECTIVES.md

The `RESPONSE_TO_OBJECTIVES.md` feature is only as good as the objectives you define. Vague objectives produce vague responses.

**Before (weak):**

```markdown
- Understand sales performance
- Look at trends
```

**After (strong):**

```markdown
1. Identify which product categories drive the most revenue, and whether their profit margins differ materially from lower-volume categories.
2. Determine whether there is a seasonal pattern in monthly order volume, and if so, in which months peaks and troughs occur.
3. Assess the data quality of the pricing columns — flag any anomalies, missing values, or implausible unit prices.
4. Compare performance across city regions and identify whether any region is significantly underperforming relative to its order volume.
```

The objectives service is prompted to provide **Evidence**, **Gaps & Recommended Analyses**, and **Interpretation** for each objective — the more specific the objective, the richer the response.

---

## 4. Tune Data Quality Detection

The dirty row detector uses hardcoded thresholds. Editing these in `src/csv_analyser/dirty_service.py` lets you tune sensitivity to your dataset.

### Outlier threshold

```python
# Line ~60 in dirty_service.py
threshold = 3 * std   # Change to 2 for stricter, 4 for looser
```

- `2 * std` — flags more rows, useful for financial data where small anomalies matter
- `3 * std` — default, balances false positives
- `4 * std` — only flags extreme outliers, useful for noisy sensor data

### Non-negative column hints

```python
# The set of column name fragments that should never contain negative values
_NON_NEGATIVE_HINTS = {
    "price", "quantity", "revenue", "sales",
    "amount", "cost", "total", "count", ...
}
```

Add domain-specific column name fragments to catch negative values that shouldn't exist in your data (e.g. `"weight"`, `"duration"`, `"age"`).

---

## 5. Improve Type Detection for Your Data

The data service uses heuristics to decide whether columns are numeric or datetime. If columns are being mis-classified, edit `src/csv_analyser/data_service.py`:

### Numeric detection threshold

```python
# Line ~47 — 80% of values must be parseable as float
NUMERIC_THRESHOLD = 0.80   # Raise to 0.95 for cleaner data, lower to 0.60 for messier
```

### Date column detection

Currently a column is treated as a date axis only if its name contains `"date"` or `"time"`. Add synonyms for your domain:

```python
# Line ~52
DATE_HINTS = {"date", "time", "month", "year", "period", "week", "quarter", "timestamp"}
```

This affects whether time-series charts are generated and how the SQL catalog treats temporal dimensions.

---

## 6. Adjust Token Budgets

Token budgets are set per-service and control how much the model can write. Raising them produces more detailed output at higher cost.

### Chart insights

```python
# src/csv_analyser/insight_service.py
MAX_TOKENS = 1_400   # Per chart
```

Increase to `2_500`–`3_000` for longer, more detailed insights. Each chart is analysed independently so this multiplies by your chart count.

The 90-word field limit in the system prompt is separate — also loosen that if you want richer insights:

```python
system_prompt = """\
...
- Keep each field <= 90 words.   # Change to 150 or remove the limit
...
"""
```

### Objectives response

```python
# src/csv_analyser/objectives_service.py
MAX_TOKENS = 16_000
```

This is already generous. Only increase if you have many objectives (10+) and are getting truncated responses.

---

## 7. Expand Conversation History in Ask AI

The Ask AI endpoint sends the last 5 exchanges as conversation history. For complex multi-step analysis sessions, increasing this improves follow-up accuracy:

```python
# src/csv_analyser/routes.py — around line 684
HISTORY_WINDOW = 5   # Increase to 10-15 for longer analytical sessions
```

Note: more history means more tokens per request and slower responses.

---

## 8. Use DEBUG Logging to Diagnose Issues

When insights or SQL queries are failing silently, enable debug logging to see every LLM call, chunk, and failure:

```env
LOG_LEVEL=DEBUG
```

This logs:
- Every LLM request (model, token count, prompt truncation)
- Every streaming chunk received
- SQL query execution results and errors
- Chart generation timing per family
- Cancellation events

Switch back to `INFO` in production to reduce noise.

---

## 9. Run the Full Claude Code SQL Workflow

Beyond `/sql-titles` and `/sql-create`, the full workflow unlocks deeper analysis:

```
/planner _ideas/kaggle_ideas.md     # Turn an idea into a research plan
/spec _plans/kaggle_plan.md         # Turn a plan into a Python spec
/execute _specs/kaggle_specs.md     # Run the spec as Python scripts
```

This pipeline lets you go from a dataset and a question to executed Python analysis with charts, statistical tests, and ML results — all grounded in your specific data.

---

## 10. Run the Agent Workflow via Claude Code Commands

The agent exposes several slash commands that orchestrate multi-step LLM work:

| Command | What it does |
|---|---|
| `/sql-titles` | Generates domain-aware SQL query titles for your dataset |
| `/sql-create output/sql/sql_title.md` | Writes and tests SQL for all titles |
| `/insights output/images` | Deep analysis of all generated chart images |
| `/solve output my_question` | Grounds an answer in charts, SQL results, and reports |
| `/dashboard` | Builds an interactive Shiny dashboard from output files |
| `/rsi` | Recursive self-improvement — analyses past sessions to tune commands and skills |

---

## 11. Provide Richer Context at Upload Time

The pipeline uses column names and row counts as LLM context. You can improve insight quality without changing any code by naming your columns descriptively before uploading.

**Before:** `col_a`, `val`, `cat1`, `dt`

**After:** `revenue_usd`, `unit_price`, `product_category`, `order_date`

Better column names result in:
- More accurate chart titles
- Better SQL query generation (the LLM can infer business meaning)
- More relevant Ask AI responses
- More specific dirty row detection (the non-negative hint matching is name-based)

---

## 12. Upgrade Models via OpenRouter

The agent routes all LLM calls through [OpenRouter](https://openrouter.ai), which gives access to models from Anthropic, OpenAI, Google, Meta, Mistral, and others — all through a single API key. You can experiment with any model listed at `openrouter.ai/models` by setting the env vars in section 1.

Free-tier models (like the current objectives default `minimax/minimax-m2.5:free`) work but have lower quality ceilings and rate limits. Switching to a paid model for objectives typically yields the most noticeable quality improvement per dollar spent.

**Current recommended models by provider (as of early 2026):**

| Provider | Best quality | Best value |
|---|---|---|
| Anthropic | `anthropic/claude-opus-4-6` | `anthropic/claude-sonnet-4-5` |
| OpenAI | `openai/gpt-4.1` | `openai/gpt-4.1-mini` |
| Google | `google/gemini-2.5-pro` | `google/gemini-2.0-flash` |
| Meta | `meta-llama/llama-4-maverick` | `meta-llama/llama-4-scout` |
| Mistral | `mistral/mistral-large-3` | `mistral/mistral-small-3` |

---

## Quick Reference: Environment Variables

```env
# Required for all LLM features
OPENROUTER_API_KEY=sk-or-...

# Model selection (change these for the biggest quality improvement)
OPENROUTER_INSIGHTS_MODEL=anthropic/claude-sonnet-4-5
OPENROUTER_OBJECTIVES_MODEL=anthropic/claude-sonnet-4-5
OPENROUTER_MODEL=anthropic/claude-sonnet-4-5

# Debugging
LOG_LEVEL=DEBUG

# CORS (add your deployed frontend URL here)
CORS_ORIGINS=http://localhost:8000,http://localhost:8001,https://your-app.example.com
```

---

## Impact Summary

| Change | Quality | Accuracy | Performance | Effort |
|---|---|---|---|---|
| Upgrade objectives model | High | High | Neutral | Low — edit `.env` |
| Run `/sql-titles` + `/sql-create` | High | High | Neutral | Low — two commands |
| Write detailed `OBJECTIVES.md` | High | High | Neutral | Low — text editing |
| Upgrade insights model | Medium–High | Medium | Slower/costlier | Low — edit `.env` |
| Raise insight token budget | Medium | Low | Slower | Low — edit one line |
| Tune outlier threshold | Low–Medium | Medium | Neutral | Low — edit one line |
| Improve column naming in CSV | Medium | Medium | Neutral | Medium — data prep |
| Add date hints for your domain | Low–Medium | Medium | Neutral | Low — edit one line |
| Enable DEBUG logging | Diagnostic | Diagnostic | Slower (I/O) | Low — edit `.env` |
