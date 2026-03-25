from __future__ import annotations

import os
from datetime import UTC, datetime
from html import escape
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from biomed_api.models.schemas import ChartArtifact


_HERE = Path(__file__).resolve().parents[3]  # project root
OBJECTIVES_PATH = _HERE / "OBJECTIVES.md"
RESPONSE_PATH = _HERE / "output" / "RESPONSE_TO_OBJECTIVES.md"
RESPONSE_HTML_PATH = _HERE / "output" / "RESPONSE_TO_OBJECTIVES.html"
DOTENV_PATH = _HERE / ".env"

load_dotenv(dotenv_path=DOTENV_PATH, override=False)

MODEL = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
MAX_TOKENS = 16_000
OPENROUTER_BASE_URL = "https://openrouter.ai/api"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _render_markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    html_parts: list[str] = []
    in_list = False

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue

        if line.startswith("---"):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("<hr />")
            continue

        if line.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h3>{escape(line[4:])}</h3>")
            continue

        if line.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h2>{escape(line[3:])}</h2>")
            continue

        if line.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h1>{escape(line[2:])}</h1>")
            continue

        if line.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{escape(line[2:])}</li>")
            continue

        if in_list:
            html_parts.append("</ul>")
            in_list = False

        if line.startswith("_") and line.endswith("_") and len(line) > 2:
            html_parts.append(f"<p><em>{escape(line[1:-1])}</em></p>")
        else:
            html_parts.append(f"<p>{escape(line)}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def _chart_index(artifacts: list[ChartArtifact]) -> str:
    if not artifacts:
        return "No charts generated yet."
    return "\n".join(f"- {a.name} ({a.category}, {a.format})" for a in artifacts)


def generate_response_to_objectives(
    chart_artifacts: list[ChartArtifact],
    objectives_path: Path | None = None,
    response_path: Path | None = None,
) -> Path:
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
    report_text = _read(_HERE / "output" / "report.md")
    insights_text = _read(_HERE / "output" / "insights" / "insights.md")
    chart_index = _chart_index(chart_artifacts)
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    system_prompt = """\
You are a senior biomedical data scientist and oncology researcher with deep expertise in \
neuroblastoma, clinical trial design, survival analysis, and translational genomics.

You will be given:
1. A set of research objectives from a neuroblastoma study.
2. Pipeline outputs: a statistical report, chart insights, and a list of generated visualisations.

Your task is to write a **rigorous, detailed scientific response** to every numbered/bulleted \
objective. For each objective:

- State clearly what the objective requires.
- Assess what the current pipeline outputs *directly address* vs. what *remains to be done*.
- Provide specific biomedical interpretation of the available findings (cohort statistics, \
  biomarker correlations, survival stratification, gene expression patterns).
- Recommend the precise statistical method(s) needed to fully address the objective \
  (e.g. log-rank test, Cox PH regression, ROC/AUC, Mann-Whitney U, LOOCV).
- Note any data quality considerations (sample size, missing data, confounders).
- Write in the style of a scientific methods/results commentary — clear, precise, and \
  technically grounded. Do not hedge unnecessarily.

Format the output as clean Markdown:
- Start with a `## TL;DR` section: 3–5 concise bullet points summarising the overall picture \
  — what the data shows, what is addressed, and the single most important next step.
- Then one `## Objective X.Y` heading per objective (matching the IDs in the objectives document).
- Use `### Current Pipeline Evidence`, `### Gaps & Recommended Analyses`, and \
  `### Biomedical Interpretation` sub-sections for each.
- End with a `## Summary Table` that lists each objective ID, a one-line status \
  (Addressed / Partially Addressed / Not Yet Addressed), and the key method needed.

Be thorough. This is a research document, not a summary.\
"""

    user_message = f"""\
## Research Objectives

{objectives_text}

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

    client = anthropic.Anthropic(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    if not response.content:
        raise RuntimeError(f"Model returned no content (stop_reason={response.stop_reason!r}).")
    text_content = next(
        (block.text for block in response.content if block.type == "text"),
        "",
    )

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
    html_body = _render_markdown_to_html(full_md)
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
