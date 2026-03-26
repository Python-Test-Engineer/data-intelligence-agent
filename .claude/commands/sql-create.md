---
description: "Read a sql_title.md file and generate SQL for every query title in it, save to output/sql/sql_queries_<table>.md, then run /sql-test all to embed results inline. Usage: /sql-create <sql_titles_file> [output_filename]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill
argument-hint: "output/sql/sql_title.md"
---

**Arguments:**
- `SQL_TITLES_FILE` — path to a sql_title.md file produced by `/sql-titles` (first token)
- `OUTPUT_FILE` — filename to save results to, without path (second token, optional)

Examples:
```
/sql-create output/sql/sql_title.md
/sql-create output/sql/sql_title.md my_queries.md
```

Parse `$ARGUMENTS`:
- `SQL_TITLES_FILE` — first token
- `OUTPUT_FILE` — second token (optional)

**If `SQL_TITLES_FILE` is missing:**
Glob `output/sql/*.md`, filter for files whose name contains `sql_title`, list them, and ask
the user to pick one.

---

## Your role

You are a senior SQL analyst. Your job is to read every query title from a catalog file and
produce a precise, correct SQL query for each one — writing all results to a single markdown
file that Claude can search and retrieve from instantly.

---

## Step 1 — Load dataset context

1. **Glob** `data/*.csv` — use the first match as the source table
2. **Read** the first 3 lines of that CSV to extract the header row (column names)
3. **Read** `SQL_TITLES_FILE` in full — this is both the source of titles AND additional
   context about the dataset's entities and measures

Derive:
- `TABLE_NAME` — CSV filename minus `.csv`, spaces/hyphens replaced with underscores
  (e.g. `sales_data_100.csv` → `sales_data_100`)
- `OUTPUT_FILE` — if not provided by the user, default to `sql_queries_<TABLE_NAME>.md`
- `OUTPUT_PATH` — always `output/sql/<OUTPUT_FILE>`

---

## Step 2 — Extract all query titles and descriptions

Parse `SQL_TITLES_FILE` to extract every numbered entry. Entries appear in two possible formats:

**With description** (produced by current `/sql-titles`):
```
1. Total Sales Revenue — Shows the combined sum of all order revenue across the entire dataset.
2. Total Revenue by Product — Ranks each product by total revenue generated, highest first.
```

**Title only** (produced by older `/sql-titles` runs):
```
1. Total Sales Revenue
2. Total Revenue by Product
```

For each entry extract:
- `TITLE` — text before ` — ` (or the full line if no ` — ` present), stripped of the leading number and period
- `DESCRIPTION` — text after ` — ` if present; otherwise leave blank and generate one in Step 3

Preserve the section groupings — you will use them to organise the output file.

Tell the user how many titles were found before proceeding.

---

## Step 3 — Generate SQL and description for every title

Work through every title in order. For each one, produce:

**SQL** — a single query following these rules:
- Use only column names present in the CSV header
- Use `TABLE_NAME` as the FROM target
- Write standard ANSI SQL (compatible with SQLite, DuckDB, PostgreSQL)
- Use `ORDER BY` where a ranked or sorted result is implied
- Use `LIMIT` only where explicitly implied (e.g. "Top 5 …")
- For titles with a variable entity (e.g. "Revenue for Customer X", "Units Sold by Product"),
  use a named placeholder: `WHERE column = :param_name` — record `param_name` as an ARG
- `ARGS` — comma-separated placeholder names, or `—` if none

**Description** — use the `DESCRIPTION` extracted from `SQL_TITLES_FILE` if present.
If the titles file had no description for this entry, generate one following these rules:
- One sentence, max 20 words
- Start with a verb: `Shows`, `Returns`, `Ranks`, `Identifies`, `Compares`, `Flags`, `Lists`
- Name the specific metric **and** dimension (e.g. "total revenue per product", not just "revenue")
- Be distinct enough that Claude can select the right query from a user's natural-language question

Process all titles before writing. Do not write the file incrementally.

---

## Step 4 — Write `OUTPUT_PATH`

Write the complete file in one operation using the **Write** tool.

### File structure

```markdown
# SQL Query Catalog
<!-- source: <CSV_FILE> | table: <TABLE_NAME> | generated: <YYYY-MM-DD> | queries: <N> -->

---

### <Section name from sql_title.md>

## <Query Title 1>
**ARGS:** <args or —>
**Description:** <one-sentence description>
```sql
<SQL>
```
---

## <Query Title 2>
**ARGS:** <args or —>
**Description:** <one-sentence description>
```sql
<SQL>
```
---
```

### Format rules (critical for fast AI retrieval)

- Every query title is a `##` heading — this is the Grep key. `Grep pattern: "## Total Revenue by Product"` returns exactly one match.
- `**ARGS:**` is always line 1 directly below the `##` heading.
- `**Description:**` is always line 2, immediately after `**ARGS:**` — no blank line between them.
- SQL is always inside a fenced ` ```sql ` block on the very next line after `**Description:**`.
- Every entry is closed with a `---` horizontal rule on its own line, no blank line before it.
- Section headings from the source file appear as `###` headings to visually group queries without conflicting with the `##` query-title grep key.
- Keep the entire entry tight — no extra blank lines anywhere inside `**ARGS:**` / `**Description:**` / code block / `---`.

---

## Step 5 — Run /sql-test all

Immediately after writing the file, run `/sql-test all` without waiting to be asked.

This will execute every query against `output/sql/data.db`, write the standalone
`_plus_results.md` file, and merge status + result rows inline into `OUTPUT_PATH` so the
final file contains queries, descriptions, pass/fail status, and output all in one place.

---

## Step 6 — Confirm

Tell the user:

```
Generated : <N> SQL queries
Table     : <TABLE_NAME>
Saved to  : <OUTPUT_PATH>
Tested    : <passed> passed · <failed> failed · <skipped> skipped
```

Then list each section name and the count of queries in it, e.g.:
```
  Revenue & Sales       9 queries
  Volume & Orders       7 queries
  ...
```

Do not print the SQL — the file contains everything.
