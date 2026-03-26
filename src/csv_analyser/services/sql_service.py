from __future__ import annotations

import datetime
import re
from pathlib import Path

import pandas as pd

from csv_analyser.services.data_service import DATA_PATH

SQL_DIR = Path("output/sql")


def _table_name(csv_path: Path) -> str:
    name = re.sub(r"[^0-9a-zA-Z]+", "_", csv_path.stem.lower())
    return re.sub(r"_+", "_", name).strip("_")


def _is_id_col(col: str) -> bool:
    low = col.lower()
    return low == "id" or low.endswith("_id")


def _entries(df: pd.DataFrame, table: str) -> list[tuple[str, str, str, str, str]]:
    """Build (section, title, description, sql, args) tuples from the DataFrame schema."""
    numeric = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and not _is_id_col(c)]
    dates = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    cats = [
        c for c in df.columns
        if not pd.api.types.is_numeric_dtype(df[c])
        and not pd.api.types.is_datetime64_any_dtype(df[c])
        and not _is_id_col(c)
        and df[c].nunique() <= 50
    ]
    ids = [c for c in df.columns if _is_id_col(c)]

    out: list[tuple[str, str, str, str, str]] = []

    # ── Overview ─────────────────────────────────────────────────────────────
    out.append((
        "Overview",
        "Row Count",
        "Returns the total number of rows in the dataset.",
        f"SELECT COUNT(*) AS row_count\nFROM {table};",
        "—",
    ))
    out.append((
        "Overview",
        "Column Sample",
        "Returns the first 10 rows to preview the dataset structure.",
        f"SELECT *\nFROM {table}\nLIMIT 10;",
        "—",
    ))

    # ── Numeric summaries ────────────────────────────────────────────────────
    for col in numeric[:6]:
        out.append((
            "Numeric Summaries",
            f"Summary Stats for {col}",
            f"Returns min, max, average, and total for {col}.",
            (
                f"SELECT\n"
                f"    MIN({col}) AS min_val,\n"
                f"    MAX({col}) AS max_val,\n"
                f"    ROUND(AVG({col}), 2) AS avg_val,\n"
                f"    SUM({col}) AS total\n"
                f"FROM {table};"
            ),
            "—",
        ))

    if numeric and cats:
        n0, c0 = numeric[0], cats[0]
        out.append((
            "Numeric Summaries",
            f"Total {n0} by {c0}",
            f"Ranks each {c0} by total {n0}, highest first.",
            f"SELECT {c0}, SUM({n0}) AS total_{n0}\nFROM {table}\nGROUP BY {c0}\nORDER BY total_{n0} DESC;",
            "—",
        ))
        out.append((
            "Numeric Summaries",
            f"Average {n0} by {c0}",
            f"Compares average {n0} across each {c0}.",
            f"SELECT {c0}, ROUND(AVG({n0}), 2) AS avg_{n0}\nFROM {table}\nGROUP BY {c0}\nORDER BY avg_{n0} DESC;",
            "—",
        ))
        if len(numeric) >= 2:
            n1 = numeric[1]
            out.append((
                "Numeric Summaries",
                f"Total {n1} by {c0}",
                f"Ranks each {c0} by total {n1}, highest first.",
                f"SELECT {c0}, SUM({n1}) AS total_{n1}\nFROM {table}\nGROUP BY {c0}\nORDER BY total_{n1} DESC;",
                "—",
            ))

    # ── Categorical distributions ─────────────────────────────────────────────
    for col in cats[:5]:
        out.append((
            "Categorical Distributions",
            f"Distribution of {col}",
            f"Counts rows for each distinct value of {col}, ordered by frequency.",
            f"SELECT {col}, COUNT(*) AS row_count\nFROM {table}\nGROUP BY {col}\nORDER BY row_count DESC;",
            "—",
        ))

    # ── Rankings ─────────────────────────────────────────────────────────────
    if numeric and cats:
        n0, c0 = numeric[0], cats[0]
        out.append((
            "Rankings",
            f"Top 10 {c0} by {n0}",
            f"Lists the 10 {c0} values with the highest total {n0}.",
            f"SELECT {c0}, SUM({n0}) AS total_{n0}\nFROM {table}\nGROUP BY {c0}\nORDER BY total_{n0} DESC\nLIMIT 10;",
            "—",
        ))
        out.append((
            "Rankings",
            f"Bottom 10 {c0} by {n0}",
            f"Lists the 10 {c0} values with the lowest total {n0}.",
            f"SELECT {c0}, SUM({n0}) AS total_{n0}\nFROM {table}\nGROUP BY {c0}\nORDER BY total_{n0} ASC\nLIMIT 10;",
            "—",
        ))
        if len(cats) >= 2:
            c1 = cats[1]
            out.append((
                "Rankings",
                f"Top 10 {c1} by {n0}",
                f"Lists the 10 {c1} values with the highest total {n0}.",
                f"SELECT {c1}, SUM({n0}) AS total_{n0}\nFROM {table}\nGROUP BY {c1}\nORDER BY total_{n0} DESC\nLIMIT 10;",
                "—",
            ))

    # ── Multi-dimensional ────────────────────────────────────────────────────
    if len(cats) >= 2 and numeric:
        n0, c0, c1 = numeric[0], cats[0], cats[1]
        out.append((
            "Multi-Dimensional",
            f"{n0} by {c0} and {c1}",
            f"Shows total {n0} broken down by both {c0} and {c1}.",
            f"SELECT {c0}, {c1}, SUM({n0}) AS total_{n0}\nFROM {table}\nGROUP BY {c0}, {c1}\nORDER BY total_{n0} DESC;",
            "—",
        ))

    # ── Parametric lookups ───────────────────────────────────────────────────
    if cats and numeric:
        c0, n0 = cats[0], numeric[0]
        out.append((
            "Parametric Lookups",
            f"Filter by {c0}",
            f"Returns all rows where {c0} matches a given value.",
            f"SELECT *\nFROM {table}\nWHERE {c0} = :{c0};",
            c0,
        ))
        out.append((
            "Parametric Lookups",
            f"Total {n0} for a Specific {c0}",
            f"Returns total {n0} for a single {c0} value.",
            (
                f"SELECT {c0}, SUM({n0}) AS total_{n0}\n"
                f"FROM {table}\n"
                f"WHERE {c0} = :{c0}\n"
                f"GROUP BY {c0};"
            ),
            c0,
        ))

    # ── Time-based ───────────────────────────────────────────────────────────
    if dates and numeric:
        d0, n0 = dates[0], numeric[0]
        out.append((
            "Time-Based Analysis",
            f"Monthly {n0} Trend",
            f"Returns total {n0} grouped by year and month.",
            (
                f"SELECT\n"
                f"    strftime('%Y-%m', {d0}) AS month,\n"
                f"    SUM({n0}) AS total_{n0}\n"
                f"FROM {table}\n"
                f"GROUP BY month\n"
                f"ORDER BY month;"
            ),
            "—",
        ))
        out.append((
            "Time-Based Analysis",
            f"Yearly {n0} Total",
            f"Returns total {n0} grouped by year.",
            (
                f"SELECT\n"
                f"    strftime('%Y', {d0}) AS year,\n"
                f"    SUM({n0}) AS total_{n0}\n"
                f"FROM {table}\n"
                f"GROUP BY year\n"
                f"ORDER BY year;"
            ),
            "—",
        ))
        out.append((
            "Time-Based Analysis",
            "Date Range Filter",
            f"Returns rows between a start and end date for {d0}.",
            f"SELECT *\nFROM {table}\nWHERE {d0} BETWEEN :start_date AND :end_date\nORDER BY {d0};",
            "start_date, end_date",
        ))

    # ── Data quality ─────────────────────────────────────────────────────────
    null_union = "\nUNION ALL\n".join(
        f"SELECT '{c}' AS column_name, COUNT(*) AS null_count FROM {table} WHERE {c} IS NULL"
        for c in list(df.columns)[:12]
    )
    out.append((
        "Data Quality Checks",
        "Missing Values per Column",
        "Counts NULL values in each column to identify data gaps.",
        null_union + "\nORDER BY null_count DESC;",
        "—",
    ))
    if ids:
        id0 = ids[0]
        out.append((
            "Data Quality Checks",
            f"Duplicate {id0} Values",
            f"Flags any {id0} that appears more than once in the dataset.",
            (
                f"SELECT {id0}, COUNT(*) AS occurrences\n"
                f"FROM {table}\n"
                f"GROUP BY {id0}\n"
                f"HAVING COUNT(*) > 1\n"
                f"ORDER BY occurrences DESC;"
            ),
            "—",
        ))
    for col in numeric[:3]:
        out.append((
            "Data Quality Checks",
            f"Negative {col} Values",
            f"Flags rows where {col} is negative, which may indicate data errors.",
            f"SELECT *\nFROM {table}\nWHERE {col} < 0\nORDER BY {col};",
            "—",
        ))

    return out


def generate_sql_catalog(df: pd.DataFrame, csv_path: Path | None = None) -> tuple[Path, Path]:
    """
    Generate sql_title.md and sql_queries_<table>.md from a DataFrame.
    Returns (sql_title_path, sql_queries_path).
    """
    src = csv_path or DATA_PATH
    table = _table_name(src)
    today = datetime.date.today().isoformat()

    entries = _entries(df, table)
    SQL_DIR.mkdir(parents=True, exist_ok=True)

    # ── sql_title.md ──────────────────────────────────────────────────────────
    title_lines: list[str] = [
        f"# SQL Query Catalog — {src.name}",
        "",
        f"Dataset: `{src}`",
        f"Columns: {', '.join(f'`{c}`' for c in df.columns)}",
        "",
        "---",
        "",
    ]
    n = 1
    current_section: str | None = None
    for section, title, desc, _sql, _args in entries:
        if section != current_section:
            if current_section is not None:
                title_lines += ["", "---", ""]
            title_lines += [f"## {section}", ""]
            current_section = section
        title_lines.append(f"{n}. {title} — {desc}")
        n += 1
    title_lines += [
        "",
        "---",
        "",
        f"*Generated from dataset inspection — {src.name} ({len(df)} rows, {len(df.columns)} columns)*",
    ]
    title_path = SQL_DIR / "sql_title.md"
    title_path.write_text("\n".join(title_lines), encoding="utf-8")

    # ── sql_queries_<table>.md ────────────────────────────────────────────────
    query_lines: list[str] = [
        "# SQL Query Catalog",
        f"<!-- source: {src.name} | table: {table} | generated: {today} | queries: {len(entries)} -->",
        "",
        "---",
        "",
    ]
    current_section = None
    for section, title, desc, sql, args in entries:
        if section != current_section:
            query_lines += [f"### {section}", ""]
            current_section = section
        query_lines += [
            f"## {title}",
            f"**ARGS:** {args}",
            f"**Description:** {desc}",
            "```sql",
            sql,
            "```",
            "---",
            "",
        ]
    queries_path = SQL_DIR / f"sql_queries_{table}.md"
    queries_path.write_text("\n".join(query_lines), encoding="utf-8")

    return title_path, queries_path
