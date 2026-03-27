from __future__ import annotations

import datetime
import re
from pathlib import Path

import pandas as pd

from csv_analyser.services.data_service import DATA_PATH

_HERE = Path(__file__).resolve().parents[3]  # project root
SQL_DIR = _HERE / "output" / "sql"


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

    # ── Multi-metric analysis ─────────────────────────────────────────────────
    # Identifies "percentage / rate" columns for AVG vs SUM columns for SUM.
    # Picks the best ordering column (profit > revenue > first numeric).
    _pct_cols = [n for n in numeric if any(k in n.lower() for k in ["pct", "rate", "margin", "ratio", "score", "avg"])]
    _sum_cols = [n for n in numeric if n not in _pct_cols]
    _sort_col = next(
        (n for n in _sum_cols if any(k in n.lower() for k in ["profit", "total_profit"])),
        next(
            (n for n in _sum_cols if any(k in n.lower() for k in ["revenue", "total_revenue"])),
            _sum_cols[0] if _sum_cols else (numeric[0] if numeric else None),
        ),
    )

    if cats and numeric and _sort_col:
        # Per-category comprehensive breakdown
        for cat in cats[:3]:
            metric_lines = ["    COUNT(*) AS transaction_count"]
            for n in _sum_cols[:6]:
                metric_lines.append(f"    SUM({n}) AS total_{n}")
            for n in _pct_cols[:3]:
                metric_lines.append(f"    ROUND(AVG({n}), 2) AS avg_{n}")
            metrics_str = ",\n".join(metric_lines)
            out.append((
                "Multi-Metric Analysis",
                f"Performance Breakdown by {cat}",
                f"Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by {cat}.",
                (
                    f"SELECT\n    {cat},\n{metrics_str}\n"
                    f"FROM {table}\n"
                    f"GROUP BY {cat}\n"
                    f"ORDER BY total_{_sort_col} DESC;"
                ),
                "—",
            ))

        # Cross-category breakdown (cat0 × cat1) with multi-metric
        if len(cats) >= 2:
            c0, c1 = cats[0], cats[1]
            metric_lines = ["    COUNT(*) AS transaction_count"]
            for n in _sum_cols[:4]:
                metric_lines.append(f"    SUM({n}) AS total_{n}")
            for n in _pct_cols[:2]:
                metric_lines.append(f"    ROUND(AVG({n}), 2) AS avg_{n}")
            metrics_str = ",\n".join(metric_lines)
            out.append((
                "Multi-Metric Analysis",
                f"{c0} × {c1} Performance Matrix",
                f"Shows performance metrics for every {c0} and {c1} combination, ordered by profitability.",
                (
                    f"SELECT\n    {c0},\n    {c1},\n{metrics_str}\n"
                    f"FROM {table}\n"
                    f"GROUP BY {c0}, {c1}\n"
                    f"ORDER BY total_{_sort_col} DESC;"
                ),
                "—",
            ))

    # Distinct ID concentration by category (e.g. unique customers per store)
    if ids and cats and _sort_col:
        id0 = ids[0]
        for cat in cats[:2]:
            out.append((
                "Multi-Metric Analysis",
                f"Unique {id0} Count by {cat}",
                f"Counts distinct {id0} values and key metrics per {cat} to reveal concentration.",
                (
                    f"SELECT\n"
                    f"    {cat},\n"
                    f"    COUNT(DISTINCT {id0}) AS unique_{id0},\n"
                    f"    COUNT(*) AS transaction_count,\n"
                    f"    SUM({_sort_col}) AS total_{_sort_col}\n"
                    f"FROM {table}\n"
                    f"GROUP BY {cat}\n"
                    f"ORDER BY unique_{id0} DESC;"
                ),
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
        # Time × category breakdown
        if cats and _sort_col:
            c0 = cats[0]
            out.append((
                "Time-Based Analysis",
                f"Monthly {_sort_col} by {c0}",
                f"Shows monthly {_sort_col} trend broken down by {c0} to reveal seasonal patterns per group.",
                (
                    f"SELECT\n"
                    f"    strftime('%Y-%m', {d0}) AS month,\n"
                    f"    {c0},\n"
                    f"    COUNT(*) AS transaction_count,\n"
                    f"    SUM({_sort_col}) AS total_{_sort_col}\n"
                    f"FROM {table}\n"
                    f"GROUP BY month, {c0}\n"
                    f"ORDER BY month, total_{_sort_col} DESC;"
                ),
                "—",
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



def get_sql_catalog_entries() -> list[dict[str, str]]:
    """Parse sql_queries_*.md and return list of {title, description, sql, args} dicts."""
    files = sorted(SQL_DIR.glob("sql_queries_*.md"))
    if not files:
        return []
    text = files[-1].read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_sql = False
    sql_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                if sql_lines:
                    current["sql"] = "\n".join(sql_lines)
                if current.get("sql"):
                    entries.append(current)
            current = {"title": line[3:].strip(), "args": "—", "description": "", "sql": ""}
            in_sql = False
            sql_lines = []
        elif current is None:
            continue
        elif line.startswith("**ARGS:**"):
            current["args"] = line.removeprefix("**ARGS:**").strip()
        elif line.startswith("**Description:**"):
            current["description"] = line.removeprefix("**Description:**").strip()
        elif line.strip() == "```sql":
            in_sql = True
            sql_lines = []
        elif line.strip() == "```" and in_sql:
            in_sql = False
        elif in_sql:
            sql_lines.append(line)

    if current is not None:
        if sql_lines:
            current["sql"] = "\n".join(sql_lines)
        if current.get("sql"):
            entries.append(current)

    return entries


def get_sql_catalog_with_results() -> list[dict[str, str]]:
    """Parse sql_queries_*.md returning entries with pre-computed test results when available."""
    files = sorted(SQL_DIR.glob("sql_queries_*.md"))
    if not files:
        return []
    queries_file = files[-1]
    text = queries_file.read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_sql = False
    post_sql = False
    sql_lines: list[str] = []
    result_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            if current is not None:
                if sql_lines:
                    current["sql"] = "\n".join(sql_lines)
                current["result"] = "\n".join(result_lines).strip()
                if current.get("sql"):
                    entries.append(current)
            current = {
                "title": stripped[3:].strip(),
                "args": "—",
                "description": "",
                "sql": "",
                "result": "",
                "source_file": queries_file.name,
            }
            in_sql = False
            post_sql = False
            sql_lines = []
            result_lines = []
        elif current is None:
            continue
        elif stripped.startswith("**ARGS:**"):
            current["args"] = line.removeprefix("**ARGS:**").strip()
        elif stripped.startswith("**Description:**"):
            current["description"] = line.removeprefix("**Description:**").strip()
        elif stripped == "```sql":
            in_sql = True
            sql_lines = []
        elif stripped == "```" and in_sql:
            in_sql = False
            post_sql = True
        elif in_sql:
            sql_lines.append(line)
        elif post_sql:
            if stripped == "---" or stripped.startswith("### "):
                post_sql = False
            else:
                result_lines.append(line)

    if current is not None:
        if sql_lines:
            current["sql"] = "\n".join(sql_lines)
        current["result"] = "\n".join(result_lines).strip()
        if current.get("sql"):
            entries.append(current)

    return entries


def run_tests_and_merge(queries_path: Path, csv_path: Path) -> dict[str, int]:
    """
    Execute every query in queries_path against csv_path via in-memory SQLite,
    write a log file alongside the queries file, and merge results inline.
    Returns {"passed": N, "failed": N, "skipped": N}.
    """
    import sqlite3

    table = _table_name(csv_path)
    df = pd.read_csv(csv_path)
    con = sqlite3.connect(":memory:")
    df.to_sql(table, con, if_exists="replace", index=False)
    con.row_factory = sqlite3.Row

    text = queries_path.read_text(encoding="utf-8")

    # Parse entries
    entries: list[dict] = []
    current_title: str | None = None
    in_sql = False
    sql_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            if current_title and sql_lines:
                entries.append({"title": current_title, "sql": "\n".join(sql_lines).strip()})
            current_title = stripped[3:].strip()
            sql_lines = []
            in_sql = False
        elif stripped == "```sql":
            in_sql = True
        elif stripped == "```" and in_sql:
            in_sql = False
        elif in_sql:
            sql_lines.append(line)
    if current_title and sql_lines:
        entries.append({"title": current_title, "sql": "\n".join(sql_lines).strip()})

    # Execute
    results: list[dict] = []
    for entry in entries:
        sql_str = entry["sql"]
        if ":" in sql_str and any(f":{w}" in sql_str for w in sql_str.split(":")):
            results.append({**entry, "status": "skipped",
                            "reason": "Query requires runtime arguments (:param)", "rows": []})
            continue
        try:
            cur = con.execute(sql_str)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
            results.append({**entry, "status": "ok", "columns": cols, "rows": rows})
        except Exception as exc:
            results.append({**entry, "status": "error", "reason": str(exc), "rows": []})
    con.close()

    passed  = sum(1 for r in results if r["status"] == "ok")
    failed  = sum(1 for r in results if r["status"] == "error")
    skipped = sum(1 for r in results if r["status"] == "skipped")

    # Write log file
    _now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _orig_csv_path = queries_path.parent / "original_csv.md"
    _orig_csv = _orig_csv_path.read_text(encoding="utf-8").split("`")[1] if _orig_csv_path.exists() else str(csv_path)
    log_lines: list[str] = [
        "# SQL Test Results",
        f"\nCreated: `{_now}`  ",
        f"Original CSV: `{_orig_csv}`  ",
        f"\nQueries file: `{queries_path}`  ",
        f"Source CSV: `{csv_path}` (in-memory SQLite)  ",
        f"Queries run: **{len(results)}** (all)\n",
        "---\n",
        f"**Summary:** {passed} passed · {failed} failed · {skipped} skipped\n",
        "---\n",
    ]
    for i, r in enumerate(results, 1):
        log_lines.append(f"## {i}. {r['title']}")
        log_lines.append(f"\n**Status:** {r['status'].upper()}\n")
        log_lines.append("```sql")
        log_lines.append(r["sql"])
        log_lines.append("```\n")
        if r["status"] == "ok":
            rows, cols = r["rows"], r.get("columns", [])
            log_lines.append(f"**Rows returned:** {len(rows)}\n")
            if rows:
                log_lines.append("| " + " | ".join(cols) + " |")
                log_lines.append("| " + " | ".join("---" for _ in cols) + " |")
                for row in rows[:20]:
                    log_lines.append("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")
                if len(rows) > 20:
                    log_lines.append(f"\n*…{len(rows) - 20} more rows not shown*")
            else:
                log_lines.append("*(no rows returned)*")
        elif r["status"] == "error":
            log_lines.append(f"**Error:** `{r['reason']}`")
        else:
            log_lines.append(f"**Skipped:** {r['reason']}")
        log_lines.append("\n---\n")

    log_path = queries_path.with_name("log_test_at_" + queries_path.stem + ".md")
    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    # Merge results inline into queries file
    result_map: dict[str, dict] = {}
    for r in results:
        body_parts = []
        if r["status"] == "ok":
            rows, cols = r["rows"], r.get("columns", [])
            body_parts.append(f"**Rows returned:** {len(rows)}\n")
            if rows:
                body_parts.append("| " + " | ".join(cols) + " |")
                body_parts.append("| " + " | ".join("---" for _ in cols) + " |")
                for row in rows[:20]:
                    body_parts.append("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")
                if len(rows) > 20:
                    body_parts.append(f"\n*…{len(rows) - 20} more rows not shown*")
            else:
                body_parts.append("*(no rows returned)*")
        elif r["status"] == "error":
            body_parts.append(f"**Error:** `{r['reason']}`")
        else:
            body_parts.append(f"**Skipped:** {r['reason']}")
        result_map[r["title"]] = {"status": r["status"].upper(), "body": "\n".join(body_parts)}

    q_lines = text.splitlines()
    out: list[str] = []
    i = 0
    cur_title: str | None = None
    in_sql2 = False
    skip_old = False
    while i < len(q_lines):
        line = q_lines[i]
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            cur_title = stripped[3:].strip()
            skip_old = False
        if stripped == "```sql":
            in_sql2 = True
            skip_old = False
            out.append(line)
            i += 1
            continue
        if stripped == "```" and in_sql2:
            in_sql2 = False
            skip_old = True
            out.append(line)
            if cur_title and cur_title in result_map:
                r = result_map[cur_title]
                out.append("")
                out.append(f"**Status:** {r['status']}")
                if r["body"]:
                    out.append("")
                    out.append(r["body"])
            i += 1
            continue
        if skip_old and (stripped == "---" or stripped.startswith("## ") or stripped.startswith("### ")):
            skip_old = False
        if skip_old:
            i += 1
            continue
        out.append(line)
        i += 1
    queries_path.write_text("\n".join(out), encoding="utf-8")

    return {"passed": passed, "failed": failed, "skipped": skipped}


def run_query_against_db(sql: str, params: dict[str, str] | None = None, limit: int = 30) -> list[dict]:
    """Execute SQL against an in-memory SQLite loaded from the source CSV."""
    import sqlite3

    if not DATA_PATH.exists():
        raise FileNotFoundError("data.csv not found — upload a CSV first.")

    table = _table_name(DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    con = sqlite3.connect(":memory:")
    df.to_sql(table, con, if_exists="replace", index=False)

    sql_core = sql.rstrip().rstrip(";")
    if "limit" not in sql_core.lower():
        sql_core += f"\nLIMIT {limit}"

    con.row_factory = sqlite3.Row
    cursor = con.execute(sql_core, params or {})
    return [dict(row) for row in cursor.fetchall()]
