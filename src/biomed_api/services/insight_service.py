from __future__ import annotations

from datetime import UTC, datetime
from html import escape
from pathlib import Path

import pandas as pd

from biomed_api.models.schemas import ChartArtifact


INSIGHTS_DIR = Path("output/insights")
FINAL_INSIGHTS_MD = INSIGHTS_DIR / "insights.md"
FINAL_INSIGHTS_HTML = INSIGHTS_DIR / "insights.html"


def _safe_title(stem: str) -> str:
    return stem.replace("_", " ").title()


def _cohort_snapshot(df: pd.DataFrame) -> list[str]:
    lines: list[str] = [
        f"- Cohort size: {len(df)}",
        f"- Variables: {len(df.columns)}",
    ]

    if "event" in df.columns:
        event_rate = pd.to_numeric(df["event"], errors="coerce").mean()
        if pd.notna(event_rate):
            lines.append(f"- Overall event rate: {float(event_rate):.2%}")

    if "efs_months" in df.columns:
        efs_median = pd.to_numeric(df["efs_months"], errors="coerce").median()
        if pd.notna(efs_median):
            lines.append(f"- Median EFS (months): {float(efs_median):.1f}")

    return lines


def _build_medical_insight(name_stem: str, df: pd.DataFrame) -> str:
    if "correlation_heatmap" in name_stem:
        expr_cols = [c for c in df.columns if c.startswith("expr_")]
        if len(expr_cols) >= 2:
            corr = df[expr_cols].corr(numeric_only=True).abs()
            max_corr = None
            for idx, col in enumerate(corr.columns):
                for peer in corr.columns[idx + 1 :]:
                    value = corr.loc[col, peer]
                    if pd.isna(value):
                        continue
                    if max_corr is None or float(value) > max_corr:
                        max_corr = float(value)
            if pd.notna(max_corr):
                return (
                    f"The strongest absolute biomarker-to-biomarker correlation appears moderate at about {float(max_corr):.2f}, "
                    "suggesting partial co-expression rather than complete redundancy."
                )
        return "The correlation map suggests how biomarkers may co-vary and may indicate groups that move together clinically."

    if "efs_by_risk" in name_stem and {"risk_group", "efs_months"}.issubset(df.columns):
        grouped = df.groupby("risk_group", dropna=False)["efs_months"].median().sort_values()
        if len(grouped) >= 2:
            low = grouped.index[0]
            high = grouped.index[-1]
            return (
                f"Median EFS differs across risk strata, with {low} showing the lowest and {high} the highest median in this sample."
            )

    if "risk_distribution" in name_stem and "risk_group" in df.columns:
        counts = df["risk_group"].fillna("<missing>").value_counts()
        if not counts.empty:
            return (
                f"The cohort is dominated by '{counts.index[0]}' risk patients ({int(counts.iloc[0])} cases), "
                "which can influence aggregate outcome interpretation."
            )

    if "km_" in name_stem:
        return "The survival-style curves illustrate time-to-event separation across groups and help identify clinically distinct trajectories."

    return "This figure provides exploratory clinical context for cohort phenotype and outcomes."


def _build_research_insight(name_stem: str, df: pd.DataFrame) -> str:
    if "correlation_heatmap" in name_stem:
        return "Use this map to reduce collinearity in downstream models and to prioritize orthogonal biomarker panels."
    if "expression_summary" in name_stem:
        return "Biomarkers with wider spread may offer stronger signal but may also reflect technical variability requiring normalization checks."
    if "mycn_vs_alk" in name_stem:
        return "The bivariate structure can motivate interaction terms and subgroup analyses around MYCN/ALK axes."
    if "event_rate_heatmap" in name_stem:
        return "Risk x MYCN event-rate cells can guide stratified hypothesis tests and sample-size planning for future validation."
    if "km_" in name_stem:
        return "Curve separation can be translated into formal survival modeling hypotheses with adjusted covariates."
    if "age_distribution" in name_stem:
        return "Age distribution informs external validity and whether age-adjusted analyses are needed."
    if "stage_distribution" in name_stem:
        return "Stage composition can confound biomarker-outcome links and should be included in multivariable analyses."
    return "This plot supports exploratory hypothesis generation and should be validated in an independent cohort."


def _build_caveat(df: pd.DataFrame) -> str:
    missing = int(df.isna().sum().sum())
    return (
        f"Insights are non-causal and exploratory. Missing cells in source data: {missing}. "
        "Measurement error, confounding, and sample-size limits may alter conclusions."
    )


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

        if line.startswith("![") and "](" in line and line.endswith(")"):
            alt_end = line.find("]")
            src_start = line.find("(", alt_end) + 1
            src = line[src_start:-1]
            alt = line[2:alt_end]
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(
                f'<p><img src="{escape(src)}" alt="{escape(alt)}" style="max-width: 100%; border: 1px solid #d0d6dd; border-radius: 10px;" /></p>'
            )
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
        html_parts.append(f"<p>{escape(line)}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def generate_insights_bundle(
    df: pd.DataFrame,
    chart_artifacts: list[ChartArtifact],
    insights_dir: str | Path | None = None,
) -> tuple[Path, Path, list[Path]]:
    target_dir = Path(insights_dir) if insights_dir is not None else INSIGHTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    png_artifacts = [artifact for artifact in chart_artifacts if artifact.format == "png"]
    section_paths: list[Path] = []

    for artifact in png_artifacts:
        stem = Path(artifact.name).stem
        section_path = target_dir / f"{stem}.md"
        image_rel_path = f"../images/{artifact.name}"
        lines = [
            f"# Insights: {_safe_title(stem)}",
            "",
            f"![{artifact.name}]({image_rel_path})",
            "",
            "## Medical Insight",
            f"- {_build_medical_insight(stem, df)}",
            "",
            "## Research Insight",
            f"- {_build_research_insight(stem, df)}",
            "",
            "## Caveat",
            f"- {_build_caveat(df)}",
            "",
        ]
        section_path.write_text("\n".join(lines), encoding="utf-8")
        section_paths.append(section_path)

    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    merged_lines: list[str] = [
        "# Final Biomedical Insights",
        "",
        f"- Generated: {generated_at}",
        f"- Individual insight files: {len(section_paths)}",
        "",
        "## Cohort Context",
        *_cohort_snapshot(df),
        "",
        "## Consolidated Chart Insights",
        "",
    ]

    for section_path in section_paths:
        merged_lines.append(f"### {section_path.stem.replace('_', ' ').title()}")
        merged_lines.append("")
        merged_lines.append(section_path.read_text(encoding="utf-8").strip())
        merged_lines.append("")

    final_md_path = target_dir / FINAL_INSIGHTS_MD.name
    final_html_path = target_dir / FINAL_INSIGHTS_HTML.name
    final_md_path.write_text("\n".join(merged_lines) + "\n", encoding="utf-8")

    html_body = _render_markdown_to_html(final_md_path.read_text(encoding="utf-8"))
    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Final Biomedical Insights</title>
  <style>
    body {{
      margin: 0;
      background: #f3f6f8;
      color: #102227;
      font-family: "Segoe UI", Arial, sans-serif;
    }}
    main {{
      width: min(980px, 100% - 28px);
      margin: 24px auto 40px;
      background: #ffffff;
      border: 1px solid #d8dfe6;
      border-radius: 14px;
      padding: 20px;
    }}
    h1, h2, h3 {{
      color: #0f3a47;
    }}
    p, li {{
      line-height: 1.5;
    }}
    ul {{
      padding-left: 20px;
    }}
  </style>
</head>
<body>
  <main>
    {html_body}
  </main>
</body>
</html>
"""
    final_html_path.write_text(html_page, encoding="utf-8")
    return final_md_path, final_html_path, section_paths


def read_final_insights(insights_path: str | Path | None = None) -> tuple[Path, str]:
    target = Path(insights_path) if insights_path is not None else FINAL_INSIGHTS_MD
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"Insights file not found at '{target}'.")
    return target, target.read_text(encoding="utf-8")
