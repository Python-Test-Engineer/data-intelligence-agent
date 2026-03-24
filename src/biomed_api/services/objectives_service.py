from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from biomed_api.models.schemas import ChartArtifact


_HERE = Path(__file__).resolve().parents[3]  # project root
OBJECTIVES_PATH = _HERE / "OBJECTIVES.md"
RESPONSE_PATH = _HERE / "output" / "RESPONSE_TO_OBJECTIVES.md"
DOTENV_PATH = _HERE / ".env"

load_dotenv(dotenv_path=DOTENV_PATH, override=False)

MODEL = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
MAX_TOKENS = 16_000
OPENROUTER_BASE_URL = "https://openrouter.ai/api"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


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
- One `## Objective X.Y` heading per objective (matching the IDs in the objectives document).
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

    header = f"# Response to Objectives\n\n_Generated: {generated_at} · Model: {MODEL}_\n\n---\n\n"
    out_path.write_text(header + text_content, encoding="utf-8")
    return out_path
