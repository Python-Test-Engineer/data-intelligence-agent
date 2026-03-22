from __future__ import annotations

from pathlib import Path

import pandas as pd

from biomed_api.models.schemas import ChartArtifact


REPORT_PATH = Path("output/report.md")


def _association_table(df: pd.DataFrame) -> list[tuple[str, float]]:
    expr_columns = [c for c in df.columns if c.startswith("expr_")]
    if not expr_columns or "efs_months" not in df.columns:
        return []

    corr_target = df[expr_columns + ["efs_months"]].corr(numeric_only=True)["efs_months"]
    corr_target = corr_target.drop(labels=["efs_months"], errors="ignore")
    corr_target = corr_target.dropna()
    top = corr_target.abs().sort_values(ascending=False).head(5).index.tolist()
    return [(marker, float(corr_target.loc[marker])) for marker in top]


def generate_report(
    df: pd.DataFrame,
    chart_artifacts: list[ChartArtifact],
    report_path: str | Path | None = None,
) -> Path:
    target = Path(report_path) if report_path is not None else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    risk_rates = {}
    if {"risk_group", "event"}.issubset(df.columns):
        risk_rates = (
            df.groupby("risk_group", dropna=False)["event"]
            .mean()
            .sort_values(ascending=False)
            .to_dict()
        )

    mycn_rates = {}
    if {"mycn_amplified", "event"}.issubset(df.columns):
        mycn_rates = (
            df.groupby("mycn_amplified", dropna=False)["event"]
            .mean()
            .sort_values(ascending=False)
            .to_dict()
        )

    marker_associations = _association_table(df)

    lines: list[str] = []
    lines.append("# Biomedical Cohort Findings")
    lines.append("")

    lines.append("## Cohort Snapshot")
    lines.append(f"- Patients: {len(df)}")
    if "age_months" in df.columns:
        lines.append(f"- Median age (months): {df['age_months'].median():.1f}")
    lines.append(f"- Variables: {len(df.columns)}")
    lines.append("")

    lines.append("## Outcome Stratification")
    lines.append("### Event rate by risk group")
    if risk_rates:
        for group, rate in risk_rates.items():
            lines.append(f"- {group}: {rate:.2%}")
    else:
        lines.append("- Risk stratification unavailable.")

    lines.append("### Event rate by MYCN")
    if mycn_rates:
        for group, rate in mycn_rates.items():
            lines.append(f"- {group}: {rate:.2%}")
    else:
        lines.append("- MYCN stratification unavailable.")
    lines.append("")

    lines.append("## Top Biomarker-EFS Associations")
    if marker_associations:
        for marker, coeff in marker_associations:
            lines.append(f"- {marker}: correlation with EFS = {coeff:.3f}")
    else:
        lines.append("- No biomarker-EFS association table available.")
    lines.append("")

    lines.append("## Chart Index")
    if chart_artifacts:
        for artifact in chart_artifacts:
            lines.append(f"- {artifact.name} ({artifact.category})")
    else:
        lines.append("- No chart artifacts were found at report generation time.")
    lines.append("")

    lines.append("## Caveats")
    lines.append(
        "- This report is exploratory and non-causal; observed associations should not be interpreted as treatment effects."
    )
    lines.append("- Missingness and measurement error may influence estimates.")

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def read_report(report_path: str | Path | None = None) -> tuple[Path, str]:
    target = Path(report_path) if report_path is not None else REPORT_PATH
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"Report file not found at '{target}'.")
    return target, target.read_text(encoding="utf-8")
