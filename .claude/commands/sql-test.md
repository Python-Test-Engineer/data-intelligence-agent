---
description: "Run the first N queries from the SQL catalog against the source CSV (via in-memory SQLite), save results to log_test_at_<queries_file>.md (excluded from ASK AI), then merge results inline into the original queries file. Usage: /sql-test [N|all]"
allowed-tools: Read, Glob, Grep, Write, Bash
argument-hint: "all"
---

**Argument:** `[N|all]` — number of queries to run, or `all` to run every query (default: 5)

Parse `$ARGUMENTS`:
- First token: if it equals `all` (case-insensitive), set `RUN_ALL=True` and `N=None`. Otherwise parse as integer; if missing or non-numeric, default to `5` and `RUN_ALL=False`.

---

## Step 1 — Locate the SQL queries file

Glob `output/sql/sql_queries_*.md` and pick the first match. Call it `QUERIES_FILE`.

If no file is found, tell the user:
> No SQL queries file found in output/sql/. Run /sql-create first.

Then stop.

---

## Step 2 — Extract queries

Read `QUERIES_FILE` in full.

Parse every query entry. Each entry follows this structure:
```
## <Title>
**ARGS:** <args>
**Description:** <description>
```sql
<SQL>
```
---
```

Extract entries in document order. For each entry collect:
- `TITLE` — text of the `## ` heading
- `SQL` — contents of the fenced ```sql block (strip the fences)

If `RUN_ALL=True`, take all entries. Otherwise take only the first `N` entries.

---

## Step 3 — Run queries against in-memory SQLite loaded from CSV

Run this Bash command, substituting the actual `QUERIES_FILE` path and `N` value:

```bash
uv run python - <<'PYEOF'
import sqlite3, pandas as pd, pathlib, re as _re

queries_file = pathlib.Path("QUERIES_FILE")
_header_text = queries_file.read_text(encoding="utf-8")

# ── Resolve CSV path and table name from the metadata comment ─────────────────
# <!-- source: data/data.csv | table: data | ... -->
_src_match  = _re.search(r"<!--.*?source:\s*(\S+?)[\s|]", _header_text)
_tbl_match  = _re.search(r"<!--.*?table:\s*(\S+?)[\s|]",  _header_text)

csv_path    = pathlib.Path(_src_match.group(1)) if _src_match else pathlib.Path("data/data.csv")
_catalog_table = _tbl_match.group(1).rstrip("|").strip() if _tbl_match else csv_path.stem.lower()

if not csv_path.exists():
    raise SystemExit(f"CSV not found: {csv_path}. Check the source path in the queries file header.")

# ── Load CSV into in-memory SQLite (no file lock, no WinError 32) ─────────────
df = pd.read_csv(csv_path)
con = sqlite3.connect(":memory:")
df.to_sql(_catalog_table, con, if_exists="replace", index=False)
con.row_factory = sqlite3.Row
_table_remap = None   # table is loaded under the catalog name — no remap needed
print(f"Loaded {len(df)} rows into in-memory table '{_catalog_table}' from {csv_path}")

# ── Parse query entries ──────────────────────────────────────────────────────
text = _header_text

entries = []
current_title = None
in_sql = False
sql_lines = []

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

RUN_ALL = RUN_ALL_VALUE
N = N_VALUE
if not RUN_ALL:
    entries = entries[:N]

# ── Execute each query ───────────────────────────────────────────────────────
results = []
for entry in entries:
    title = entry["title"]
    sql   = entry["sql"]
    # Substitute table name if the catalog was generated for a different CSV
    if _table_remap:
        import re as _re2
        sql = _re2.sub(r'\b' + _re2.escape(_table_remap[0]) + r'\b', _table_remap[1], sql)
    # Skip queries with named placeholders (:param) — they require arguments
    if ":" in sql and any(f":{w}" in sql for w in sql.split(":")):
        results.append({"title": title, "sql": sql, "status": "skipped",
                        "reason": "Query requires runtime arguments (:param)", "rows": []})
        continue
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        results.append({"title": title, "sql": sql, "status": "ok",
                        "columns": cols, "rows": rows})
    except Exception as e:
        results.append({"title": title, "sql": sql, "status": "error",
                        "reason": str(e), "rows": []})

con.close()

# ── Format markdown output ───────────────────────────────────────────────────
lines = []
lines.append("# SQL Test Results")
lines.append(f"\nQueries file: `{queries_file}`  ")
lines.append(f"Source CSV: `{csv_path}` (in-memory SQLite)  ")
scope_label = "all" if RUN_ALL else f"first {N} of file"
lines.append(f"Queries run: **{len(results)}** ({scope_label})\n")
lines.append("---\n")

passed = sum(1 for r in results if r["status"] == "ok")
failed = sum(1 for r in results if r["status"] == "error")
skipped = sum(1 for r in results if r["status"] == "skipped")

lines.append(f"**Summary:** {passed} passed · {failed} failed · {skipped} skipped\n")
lines.append("---\n")

for i, r in enumerate(results, 1):
    lines.append(f"## {i}. {r['title']}")
    lines.append(f"\n**Status:** {r['status'].upper()}\n")
    lines.append("```sql")
    lines.append(r["sql"])
    lines.append("```\n")

    if r["status"] == "ok":
        rows = r["rows"]
        cols = r.get("columns", [])
        lines.append(f"**Rows returned:** {len(rows)}\n")
        if rows:
            # Markdown table
            lines.append("| " + " | ".join(cols) + " |")
            lines.append("| " + " | ".join("---" for _ in cols) + " |")
            for row in rows[:20]:   # cap at 20 rows in output
                cells = [str(row.get(c, "")) for c in cols]
                lines.append("| " + " | ".join(cells) + " |")
            if len(rows) > 20:
                lines.append(f"\n*…{len(rows) - 20} more rows not shown*")
        else:
            lines.append("*(no rows returned)*")
    elif r["status"] == "error":
        lines.append(f"**Error:** `{r['reason']}`")
    else:
        lines.append(f"**Skipped:** {r['reason']}")

    lines.append("\n---\n")

output = queries_file.with_name("log_test_at_" + queries_file.stem + ".md")
output.write_text("\n".join(lines), encoding="utf-8")
print(f"Written: {output}  ({passed} passed, {failed} failed, {skipped} skipped)")
PYEOF
```

**Before running**, make three substitutions in the heredoc:
- Replace `QUERIES_FILE` with the actual path found in Step 1 (e.g. `output/sql/sql_queries_data.md`)
- Replace `RUN_ALL_VALUE` with `True` if the argument was `all`, otherwise `False`
- Replace `N_VALUE` with the actual integer value of `N`, or `0` when `RUN_ALL=True` (unused but must be valid Python)

---

## Step 4 — Merge results into the original queries file

Run this Bash command, substituting the actual `QUERIES_FILE` path:

```bash
uv run python - <<'PYEOF'
import pathlib, re

queries_file = pathlib.Path("QUERIES_FILE")
results_file = queries_file.with_name("log_test_at_" + queries_file.stem + ".md")

queries_text = queries_file.read_text(encoding="utf-8")
results_text = results_file.read_text(encoding="utf-8")

# ── Parse results into a dict keyed by title ─────────────────────────────────
result_map = {}
result_blocks = re.split(r'\n(?=## \d+\.)', results_text)
for block in result_blocks:
    m = re.match(r'## \d+\.\s+(.+)', block)
    if not m:
        continue
    title = m.group(1).strip()
    status_m = re.search(r'\*\*Status:\*\*\s+(\S+)', block)
    status = status_m.group(1) if status_m else "UNKNOWN"
    after_sql = re.split(r'```\n', block, maxsplit=2)
    result_body = after_sql[-1].strip() if len(after_sql) >= 2 else ""
    result_body = re.sub(r'\n---\s*$', '', result_body).strip()
    result_map[title] = {"status": status, "body": result_body}

# ── Rebuild the queries file, stripping old results then injecting fresh ones ─
# First strip any previously merged results (between ``` and next ## / ### / ---)
lines = queries_text.splitlines()
out = []
i = 0
current_title = None
in_sql = False
skip_old_results = False

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if stripped.startswith("## ") and not stripped.startswith("### "):
        current_title = stripped[3:].strip()
        skip_old_results = False

    if stripped == "```sql":
        in_sql = True
        skip_old_results = False
        out.append(line)
        i += 1
        continue

    if stripped == "```" and in_sql:
        in_sql = False
        skip_old_results = True   # skip lines until the next entry boundary
        out.append(line)
        # Inject fresh results
        if current_title and current_title in result_map:
            r = result_map[current_title]
            out.append("")
            out.append(f"**Status:** {r['status']}")
            if r["body"]:
                out.append("")
                out.append(r["body"])
        i += 1
        continue

    # Once we hit a section boundary (---, ##, ###) after a SQL block, stop skipping
    if skip_old_results and (stripped == "---" or stripped.startswith("## ") or stripped.startswith("### ")):
        skip_old_results = False

    if skip_old_results:
        i += 1
        continue

    out.append(line)
    i += 1

queries_file.write_text("\n".join(out), encoding="utf-8")
print(f"Merged {len(result_map)} results into {queries_file}")
PYEOF
```

**Before running**, replace `QUERIES_FILE` with the actual path found in Step 1.

---

## Step 5 — Confirm

Tell the user:
- How many queries ran / passed / failed / skipped
- That results have been merged inline into the original queries file
- Path to standalone results log: `log_test_at_` prepended to the queries filename (e.g. `output/sql/log_test_at_sql_queries_sales_data_20.md`)
- For any failed queries: the title and the error message
