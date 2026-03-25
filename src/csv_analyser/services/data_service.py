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
    df = _coerce_column_types(df)
    return df


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
    cols_lower = [c.lower() for c in df.columns]
    cols_joined = " ".join(cols_lower)

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    cat_cols = [
        c for c in df.columns
        if not pd.api.types.is_numeric_dtype(df[c])
        and not pd.api.types.is_datetime64_any_dtype(df[c])
    ]

    n, p = len(df), len(df.columns)

    # Domain detection
    is_sales = any(k in cols_joined for k in ["order", "product", "customer", "price", "quantity", "store", "sale"])
    is_web = any(k in cols_joined for k in ["session", "pageview", "page_view", "visitor", "bounce", "traffic", "click", "url"])
    is_finance = any(k in cols_joined for k in ["revenue", "profit", "expense", "budget", "invoice", "payment", "transaction"])
    is_hr = any(k in cols_joined for k in ["employee", "salary", "department", "hire", "headcount"])
    is_geo = any(k in cols_joined for k in ["city", "country", "region", "state", "latitude", "longitude"])

    if is_sales:
        domain = "sales"
    elif is_web:
        domain = "web analytics"
    elif is_finance:
        domain = "financial"
    elif is_hr:
        domain = "HR / workforce"
    else:
        domain = "tabular"

    parts = [f"This appears to be a **{domain}** dataset with **{n} rows** and **{p} columns**."]

    if numeric_cols:
        sample = numeric_cols[:5]
        extra = f" (and {len(numeric_cols) - 5} more)" if len(numeric_cols) > 5 else ""
        parts.append(
            f"{len(numeric_cols)} numeric column(s) detected ({', '.join(sample)}{extra}), "
            "suitable for statistical summaries and correlation analysis."
        )

    if date_cols:
        parts.append(
            f"Date/time column(s) found ({', '.join(date_cols)}), enabling trend and time-series analysis."
        )

    if cat_cols:
        low_card = [c for c in cat_cols if 2 <= df[c].nunique() <= 30]
        if low_card:
            parts.append(
                f"{len(low_card)} categorical column(s) with manageable cardinality "
                f"({', '.join(low_card[:4])}{'...' if len(low_card) > 4 else ''}) are available for grouping and distribution charts."
            )

    if is_geo:
        parts.append("Geographic columns detected, supporting location-based breakdowns.")

    return " ".join(parts)


def build_summary(df: pd.DataFrame) -> dict[str, object]:
    row_count = len(df)
    column_count = len(df.columns)
    total_cells = row_count * max(column_count, 1)
    missing_cells = int(df.isna().sum().sum())
    missing_pct = (missing_cells / total_cells) * 100 if total_cells else 0.0

    distributions: dict[str, dict[str, int]] = {}
    for col in df.columns:
        if (
            not pd.api.types.is_numeric_dtype(df[col])
            and not pd.api.types.is_datetime64_any_dtype(df[col])
        ):
            nunique = df[col].nunique()
            if 2 <= nunique <= 20:
                counts = df[col].fillna("<missing>").value_counts(dropna=False).to_dict()
                distributions[col] = {str(k): int(v) for k, v in counts.items()}
                if len(distributions) >= 5:
                    break

    return {
        "row_count": row_count,
        "column_count": column_count,
        "missing_cells": missing_cells,
        "missing_pct": missing_pct,
        "columns": infer_schema(df),
        "key_distributions": distributions,
        "description": infer_dataset_description(df),
    }
