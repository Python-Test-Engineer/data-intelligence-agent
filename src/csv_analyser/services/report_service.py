from __future__ import annotations

from pathlib import Path

import pandas as pd

from csv_analyser.models.schemas import ChartArtifact


REPORT_PATH = Path("output/report.md")


def generate_report(
    df: pd.DataFrame,
    chart_artifacts: list[ChartArtifact],
    report_path: str | Path | None = None,
) -> Path:
    target = Path(report_path) if report_path is not None else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    cat_cols = [
        c for c in df.columns
        if not pd.api.types.is_numeric_dtype(df[c])
        and not pd.api.types.is_datetime64_any_dtype(df[c])
    ]

    lines: list[str] = []
    lines.append("# CSV Dataset Report")
    lines.append("")

    lines.append("## Dataset Snapshot")
    lines.append(f"- Rows: {len(df)}")
    lines.append(f"- Columns: {len(df.columns)}")
    lines.append(f"- Numeric columns: {len(numeric_cols)}")
    lines.append(f"- Categorical columns: {len(cat_cols)}")
    if date_cols:
        lines.append(f"- Date/time columns: {', '.join(date_cols)}")
    missing_cells = int(df.isna().sum().sum())
    lines.append(f"- Missing cells: {missing_cells}")
    lines.append("")

    lines.append("## Numeric Summary")
    if numeric_cols:
        for col in numeric_cols[:8]:
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(series) > 0:
                lines.append(
                    f"- **{col}**: mean={series.mean():.2f}, "
                    f"std={series.std():.2f}, "
                    f"min={series.min():.2f}, "
                    f"max={series.max():.2f}, "
                    f"median={series.median():.2f}"
                )
    else:
        lines.append("- No numeric columns detected.")
    lines.append("")

    lines.append("## Top Category Distributions")
    cat_shown = 0
    for col in cat_cols:
        if cat_shown >= 5:
            break
        nunique = df[col].nunique()
        if 2 <= nunique <= 30:
            counts = df[col].fillna("<missing>").value_counts().head(5)
            lines.append(f"### {col} (top {len(counts)} of {nunique} unique values)")
            for val, cnt in counts.items():
                pct = cnt / len(df) * 100
                lines.append(f"- {val}: {cnt} ({pct:.1f}%)")
            cat_shown += 1
    if cat_shown == 0:
        lines.append("- No categorical columns with suitable cardinality detected.")
    lines.append("")

    if len(numeric_cols) >= 2:
        lines.append("## Top Correlations")
        corr = df[numeric_cols].corr(numeric_only=True)
        pairs: list[tuple[str, str, float]] = []
        for i, c1 in enumerate(corr.columns):
            for c2 in corr.columns[i + 1:]:
                val = corr.loc[c1, c2]
                if pd.notna(val):
                    pairs.append((c1, c2, float(val)))
        pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        for c1, c2, val in pairs[:5]:
            lines.append(f"- {c1} vs {c2}: r = {val:.3f}")
        lines.append("")

    lines.append("## Chart Index")
    if chart_artifacts:
        for artifact in chart_artifacts:
            lines.append(f"- {artifact.name} ({artifact.category})")
    else:
        lines.append("- No chart artifacts found at report generation time.")
    lines.append("")

    lines.append("## Caveats")
    lines.append(
        "- This report is exploratory. Observed patterns should be validated before drawing conclusions."
    )
    lines.append("- Missingness and data quality may influence results.")

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def read_report(report_path: str | Path | None = None) -> tuple[Path, str]:
    target = Path(report_path) if report_path is not None else REPORT_PATH
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"Report file not found at '{target}'.")
    return target, target.read_text(encoding="utf-8")
