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
    }
