from __future__ import annotations

import logging
import os
import re
import threading
from datetime import UTC, datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

from csv_analyser.config import OUTPUT_DIR, PROJECT_ROOT
from csv_analyser.models.schemas import ChartArtifact
from csv_analyser.utils.html import render_markdown_to_html


logger = logging.getLogger(__name__)

OBJECTIVES_PATH = PROJECT_ROOT / "OBJECTIVES.md"
RESPONSE_PATH = OUTPUT_DIR / "RESPONSE_TO_OBJECTIVES.md"
RESPONSE_HTML_PATH = OUTPUT_DIR / "RESPONSE_TO_OBJECTIVES.html"
DOTENV_PATH = PROJECT_ROOT / ".env"
_SQL_DIR = OUTPUT_DIR / "sql"

load_dotenv(dotenv_path=DOTENV_PATH, override=False)

MODEL = os.environ.get(
    "OPENROUTER_OBJECTIVES_MODEL",
    os.environ.get("OPENROUTER_MODEL", "minimax/minimax-m2.5:free"),
)
MAX_TOKENS = 16_000
OPENROUTER_BASE_URL = "https://openrouter.ai/api"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_sql_catalog() -> str:
    """Return the content of the SQL queries file (with inline results if present)."""
    files = sorted(_SQL_DIR.glob("sql_queries_*.md"))
    return files[-1].read_text(encoding="utf-8") if files else ""


def count_objectives(text: str) -> int:
    """Count distinct objectives in text regardless of format."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    bullets = [line for line in lines if line.startswith("- ") or line.startswith("* ")]
    if bullets:
        return len(bullets)
    numbered = [line for line in lines if re.match(r"^\d+[.):]", line)]
    if numbered:
        return len(numbered)
    # Free-form prose: count non-empty paragraphs
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return len(paragraphs)



def _chart_index(artifacts: list[ChartArtifact]) -> str:
    if not artifacts:
        return "No charts generated yet."
    return "\n".join(f"- {a.name} ({a.category}, {a.format})" for a in artifacts)


def generate_response_to_objectives(
    chart_artifacts: list[ChartArtifact],
    objectives_path: Path | None = None,
    response_path: Path | None = None,
    cancel_event: threading.Event | None = None,
) -> tuple[Path, Path]:
    obj_path = objectives_path or OBJECTIVES_PATH
    out_path = response_path or RESPONSE_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. "
            "Set it as an environment variable before starting the server."
        )

    objectives_text = _read(obj_path)
    if not objectives_text.strip():
        raise RuntimeError(
            "OBJECTIVES.md is empty. Add your analysis objectives before generating a response."
        )

    report_text = _read(OUTPUT_DIR / "report.md")
    insights_text = _read(OUTPUT_DIR / "insights" / "insights.md")
    sql_catalog_text = _read_sql_catalog()
    chart_index = _chart_index(chart_artifacts)
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    n_objectives = count_objectives(objectives_text)

    system_prompt = f"""\
You are a senior data analyst with deep expertise in exploratory data analysis, \
statistical modelling, data visualisation, and business intelligence.

You will be given:
1. Analysis objectives — these may be numbered/bulleted lists OR free-form prose. \
   There are {n_objectives} distinct objective(s) to address.
2. Pipeline outputs: a statistical report, chart insights, a list of generated visualisations, \
   and a SQL query catalog with pre-computed results against the dataset.

Your task is to write a **rigorous, detailed response** to every objective. \
Parse the objectives carefully regardless of format. For each objective:

- Restate it clearly as a heading so the reader knows which objective is being addressed.
- Assess what the current pipeline outputs *directly address* vs. what *remains to be done*.
- Provide specific data interpretation of the available findings (summary statistics, \
  distributions, correlations, trends, category breakdowns). \
  Cite exact values from the SQL query results where available.
- Recommend the precise analytical method(s) needed to fully address the objective.
- Note any data quality considerations (sample size, missing data, outliers, confounders).
- Write in the style of a professional data analysis report — clear, precise, and technically grounded.

If no pipeline report or insights are available, say so clearly and work only from the objective text.

Format the output as clean Markdown:
- Start with a `## TL;DR` section: 3–5 bullet points — what the data shows, what is addressed, \
  and the single most important next step.
- Then one `## Objective N` heading per objective.
- Use `### Evidence`, `### Gaps & Recommended Analyses`, and `### Interpretation` sub-sections.
- End with a `## Summary Table` listing each objective, its status \
  (Addressed / Partially Addressed / Not Yet Addressed), and the key next step.

Be thorough. This is a professional analysis document.\
"""

    user_message = f"""\
## Analysis Objectives

{objectives_text}

---

## SQL Query Catalog (with pre-computed results)

{sql_catalog_text if sql_catalog_text else "No SQL catalog available. Upload a CSV to generate one."}

---

## Pipeline Report

{report_text if report_text else "No report generated yet."}

---

## Pipeline Insights

{insights_text if insights_text else "No insights generated yet."}

---

## Generated Charts

{chart_index}

---

Please write the full detailed Response to Objectives document now.\
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }
    resp = httpx.post(
        f"{OPENROUTER_BASE_URL}/v1/messages",
        json=body,
        headers=headers,
        timeout=120.0,
    )
    try:
        data = resp.json()
    except ValueError:
        data = {"error": {"message": resp.text}}
    if not resp.is_success or data.get("type") == "error":
        err = data.get("error", {})
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {err.get('message', data)}")
    if cancel_event and cancel_event.is_set():
        raise RuntimeError("Pipeline cancelled.")
    blocks = data.get("content", [])
    text_content = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")

    if not text_content.strip():
        raise RuntimeError("Model returned no content.")

    objectives_block = (
        f"## Original Objectives\n\n{objectives_text}\n\n---\n\n"
        if objectives_text.strip()
        else ""
    )
    header = (
        f"# Response to Objectives\n\n"
        f"_Generated: {generated_at} · Model: {MODEL}_\n\n"
        f"---\n\n"
        f"{objectives_block}"
    )
    full_md = header + text_content
    out_path.write_text(full_md, encoding="utf-8")

    html_path = out_path.with_suffix(".html")
    html_body = render_markdown_to_html(full_md)
    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Response to Objectives</title>
  <style>
    body {{
      margin: 0;
      background: #f5f4ee;
      color: #111111;
      font-family: "Segoe UI", Arial, sans-serif;
    }}
    main {{
      width: min(980px, 100% - 28px);
      margin: 24px auto 40px;
      background: #fcfbf8;
      border: 1px solid #d8d4c8;
      border-radius: 14px;
      padding: 24px 28px;
    }}
    h1 {{ color: #0f3a47; font-size: 1.55rem; margin-bottom: 4px; }}
    h2 {{ color: #0f3a47; border-bottom: 1px solid #d8d4c8; padding-bottom: 4px; }}
    h3 {{ color: #1f4a63; }}
    p, li {{ line-height: 1.65; }}
    ul {{ padding-left: 20px; }}
    hr {{ border: none; border-top: 1px solid #d8d4c8; margin: 16px 0; }}
    em {{ color: #4a4945; font-style: italic; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 0.92rem; }}
    th, td {{ border: 1px solid #c8c4b8; padding: 8px 12px; text-align: left; }}
    thead {{ background: #0f3a47; color: #ffffff; }}
    tbody tr:nth-child(even) {{ background: #f0ede4; }}
    code {{ background: #eeeae0; padding: 1px 5px; border-radius: 4px; font-size: 0.88em; }}
    .toolbar {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 16px;
    }}
    .download-btn {{
      display: inline-block;
      text-decoration: none;
      background: #1f4a63;
      color: #ffffff;
      padding: 9px 14px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.9rem;
    }}
    .download-btn:hover {{ opacity: 0.92; }}
  </style>
</head>
<body>
  <main>
    <div class="toolbar">
      <a class="download-btn" href="RESPONSE_TO_OBJECTIVES.md" download="RESPONSE_TO_OBJECTIVES.md">Download Markdown</a>
    </div>
    {html_body}
  </main>
</body>
</html>
"""
    html_path.write_text(html_page, encoding="utf-8")
    return out_path, html_path
