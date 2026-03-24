from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/data.csv")


def normalize_column_name(name: str) -> str:
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip().lower())
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "column"


def _dedupe_columns(columns: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    output: list[str] = []
    for col in columns:
        base = normalize_column_name(col)
        if base not in counts:
            counts[base] = 0
            output.append(base)
            continue
        counts[base] += 1
        output.append(f"{base}_{counts[base]}")
    return output


def _coerce_column_types(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in result.columns:
        series = result[column]
        if pd.api.types.is_numeric_dtype(series) or pd.api.types.is_datetime64_any_dtype(series):
            continue

        non_null_count = int(series.notna().sum())
        if non_null_count == 0:
            continue

        numeric_try = pd.to_numeric(series, errors="coerce")
        numeric_ratio = float(numeric_try.notna().sum()) / float(non_null_count)
        if numeric_ratio >= 0.8:
            result[column] = numeric_try
            continue

        parse_dates = "date" in column or "time" in column
        if parse_dates:
            datetime_try = pd.to_datetime(series, errors="coerce")
            dt_ratio = float(datetime_try.notna().sum()) / float(non_null_count)
            if dt_ratio >= 0.8:
                result[column] = datetime_try

    return result


def load_dataset(path: str | Path | None = None) -> pd.DataFrame:
    target_path = Path(path) if path is not None else DATA_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Dataset file not found at '{target_path}'.")

    df = pd.read_csv(target_path)
    df = df.rename(columns=dict(zip(df.columns, _dedupe_columns(list(df.columns)), strict=False)))
    return _coerce_column_types(df)


def infer_schema(df: pd.DataFrame) -> list[dict[str, str | int | float]]:
    profiles: list[dict[str, str | int | float]] = []
    total_rows = max(len(df), 1)
    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        profiles.append(
            {
                "name": col,
                "dtype": str(df[col].dtype),
                "missing_count": missing_count,
                "missing_pct": round((missing_count / total_rows) * 100, 2),
            }
        )
    return profiles


def infer_dataset_description(df: pd.DataFrame) -> str:
    cols = set(c.lower() for c in df.columns)
    all_cols = [c.lower() for c in df.columns]

    expr_cols = [c for c in df.columns if c.lower().startswith("expr_")]
    has_survival = bool({"efs_months", "os_months", "event", "os_event"} & cols)
    has_expression = len(expr_cols) > 0
    has_biomarkers = any(k in " ".join(all_cols) for k in ["ldh", "ferritin", "nse"])
    has_genomics = bool({"ploidy", "del_1p", "gain_17q", "aberration_11q", "seg_chr_aberrations"} & cols)
    has_treatment = bool({"treatment", "response_category", "histology"} & cols)
    has_demographics = bool({"age_months", "age", "sex", "weight_kg"} & cols)
    is_neuroblastoma = bool({"mycn_amplified", "risk_group", "stage"} & cols) or any("mycn" in c for c in all_cols)
    is_oncology = is_neuroblastoma or bool({"tumor", "cancer", "stage", "risk_group"} & cols)

    n, p = len(df), len(df.columns)

    if is_neuroblastoma:
        domain = "neuroblastoma oncology"
    elif is_oncology:
        domain = "oncology"
    else:
        domain = "biomedical"

    parts = [f"This appears to be a **{domain}** dataset with **{n} patient records** and **{p} variables**."]

    if is_neuroblastoma:
        parts.append(
            "The column structure is consistent with a neuroblastoma cohort — including INRG disease staging, "
            "risk group stratification (low / intermediate / high), and MYCN amplification status."
        )

    if has_survival:
        sv = [c for c in df.columns if c.lower() in {"efs_months", "os_months", "event", "os_event"}]
        parts.append(
            f"Survival endpoints are present ({', '.join(sv)}), making this suitable for "
            "Kaplan-Meier, log-rank, and Cox proportional-hazards analyses."
        )

    if has_expression:
        parts.append(
            f"{len(expr_cols)} gene expression features (log₂-scale) are included, covering "
            "oncogenes and tumour suppressors relevant to neuroblastoma biology."
        )

    if has_biomarkers:
        bm = [c for c in df.columns if any(k in c.lower() for k in ["ldh", "ferritin", "nse"])]
        parts.append(f"Serum biomarkers ({', '.join(bm)}) are available for prognostic and ROC analyses.")

    if has_genomics:
        parts.append(
            "Genomic aberration flags (ploidy, chromosomal deletions/gains) support molecular subgrouping."
        )

    if has_demographics and has_treatment:
        parts.append(
            "Clinical metadata — demographics, treatment allocation, and response categories — "
            "are available for multivariable modelling."
        )

    if not is_oncology and not has_survival and not has_expression:
        parts.append("No recognised clinical outcome or expression columns were detected; domain-specific interpretation may require manual review.")

    return " ".join(parts)


def build_summary(df: pd.DataFrame) -> dict[str, object]:
    row_count = len(df)
    column_count = len(df.columns)
    total_cells = row_count * max(column_count, 1)
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells) * 100, 2) if total_cells else 0.0

    distributions: dict[str, dict[str, int]] = {}
    for col in ("risk_group", "stage", "event"):
        if col in df.columns:
            counts = df[col].fillna("<missing>").value_counts(dropna=False).to_dict()
            distributions[col] = {str(k): int(v) for k, v in counts.items()}

    return {
        "row_count": row_count,
        "column_count": column_count,
        "missing_cells": missing_cells,
        "missing_pct": missing_pct,
        "columns": infer_schema(df),
        "key_distributions": distributions,
        "description": infer_dataset_description(df),
    }
