from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("output")
DIRTY_CSV_PATH = OUTPUT_DIR / "dirty.csv"
DIRTY_MD_PATH = OUTPUT_DIR / "dirty_rows.md"

# Column name hints that imply values must be non-negative
_NON_NEGATIVE_HINTS = {
    "price", "cost", "quantity", "qty", "total", "revenue", "amount",
    "count", "sales", "profit", "units", "volume", "age", "duration",
    "distance", "height", "weight", "score",
}


def _should_be_non_negative(col: str) -> bool:
    col_lower = col.lower()
    return any(hint in col_lower for hint in _NON_NEGATIVE_HINTS)


def find_dirty_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[int, list[str]]]:
    """
    Returns (dirty_df, reasons) where reasons maps original row index -> list of reason strings.

    Dirty criteria:
    1. Missing values   — one or more cells are null/NaN
    2. Exact duplicate  — row is an exact copy of a previous row
    3. Numeric outlier  — value is outside +/- 3 standard deviations from the column mean
    4. Negative value   — numeric value is negative in a column whose name implies non-negative
    """
    reasons: dict[int, list[str]] = {}

    # 1. Missing values
    for idx in df.index[df.isna().any(axis=1)]:
        missing_cols = [col for col in df.columns if pd.isna(df.at[idx, col])]
        reasons.setdefault(idx, []).append(
            f"Missing value(s) in column(s): {', '.join(missing_cols)}"
        )

    # 2. Exact duplicates (keep first occurrence, flag subsequent)
    dup_mask = df.duplicated(keep="first")
    for idx in df.index[dup_mask]:
        reasons.setdefault(idx, []).append("Exact duplicate of a previous row")

    # 3. Numeric outliers +/-3 std dev and 4. Negative values in non-negative columns
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors="coerce")
        mean = series.mean()
        std = series.std()

        if pd.notna(mean) and pd.notna(std) and std > 0:
            outlier_mask = ((series - mean).abs() > 3 * std) & series.notna()
            for idx in df.index[outlier_mask]:
                val = float(series[idx])
                reasons.setdefault(idx, []).append(
                    f"Outlier in '{col}': {val:.4g} "
                    f"(mean={mean:.4g}, +/-3 std dev threshold=[{mean - 3*std:.4g}, {mean + 3*std:.4g}])"
                )

        if _should_be_non_negative(col):
            neg_mask = (series < 0) & series.notna()
            for idx in df.index[neg_mask]:
                val = float(series[idx])
                reasons.setdefault(idx, []).append(
                    f"Negative value in '{col}': {val:.4g} (expected ≥ 0)"
                )

    dirty_df = df.loc[sorted(reasons.keys())].copy() if reasons else df.iloc[0:0].copy()
    return dirty_df, reasons


def save_dirty_report(
    df: pd.DataFrame,
    output_dir: str | Path | None = None,
) -> tuple[Path, Path]:
    out = Path(output_dir) if output_dir is not None else OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    csv_path = out / "dirty.csv"
    md_path = out / "dirty_rows.md"

    dirty_df, reasons = find_dirty_rows(df)

    # --- Save dirty.csv ---
    dirty_df.to_csv(csv_path, index=True)

    # --- Aggregate reason-type counts ---
    n_missing = sum(1 for v in reasons.values() if any("Missing" in r for r in v))
    n_dup = sum(1 for v in reasons.values() if any("duplicate" in r for r in v))
    n_outlier = sum(1 for v in reasons.values() if any("Outlier" in r for r in v))
    n_negative = sum(1 for v in reasons.values() if any("Negative" in r for r in v))

    lines: list[str] = [
        "# Dirty Row Report",
        "",
        f"- **Total rows in dataset:** {len(df)}",
        f"- **Dirty rows identified:** {len(dirty_df)}",
        f"- **Clean rows:** {len(df) - len(dirty_df)}",
        "",
        "## Criteria Used",
        "",
        "A row is flagged as **dirty** if it satisfies one or more of the following conditions:",
        "",
        "| # | Criterion | Description |",
        "|---|-----------|-------------|",
        "| 1 | **Missing value** | One or more cells are null / NaN |",
        "| 2 | **Exact duplicate** | Row is an identical copy of an earlier row |",
        "| 3 | **Numeric outlier** | A numeric value falls outside +/- 3 standard deviations from the column mean |",
        "| 4 | **Negative in non-negative column** | A numeric value is negative in a column whose name implies non-negative values (price, quantity, total, etc.) |",
        "",
    ]

    if not reasons:
        lines += [
            "## Result",
            "",
            "No dirty rows were detected. The dataset appears clean.",
        ]
    else:
        lines += [
            "## Summary by Criterion",
            "",
        ]
        if n_missing:
            lines.append(f"- **Missing values:** {n_missing} row(s)")
        if n_dup:
            lines.append(f"- **Exact duplicates:** {n_dup} row(s)")
        if n_outlier:
            lines.append(f"- **Numeric outliers (+/-3 std dev):** {n_outlier} row(s)")
        if n_negative:
            lines.append(f"- **Negative in non-negative column:** {n_negative} row(s)")

        lines += [
            "",
            "## Row-by-Row Detail",
            "",
        ]
        for idx in sorted(reasons.keys()):
            lines.append(f"### Row {idx}")
            for reason in reasons[idx]:
                lines.append(f"- {reason}")
            lines.append("")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return csv_path, md_path
