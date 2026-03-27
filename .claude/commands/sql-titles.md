---
description: "Examine a CSV and generate a categorised list of useful SQL query titles in natural language. Usage: /sql-titles [csv_file]"
allowed-tools: Read, Glob, Grep, Write, Bash
argument-hint: "data/data.csv"
---

Parse `$ARGUMENTS`:
- `CSV_FILE` — first token (path to the CSV file)

If missing or empty: default to `data/data.csv`. If `data/data.csv` does not exist, glob `data/*.csv`, list available files, and ask the user to pick one.

---

## Your role

You are a senior data analyst. Your job is to examine a CSV dataset and produce a
comprehensive, categorised catalog of useful SQL query titles — each paired with a concise
description that tells `/sql-create` exactly what SQL to generate and tells a user exactly
what question the query answers.

---

## Step 1 — Read the CSV

Read `CSV_FILE` using the Read tool.

Extract:
- **Column names** and their inferred data types (numeric, text, date, id, etc.)
- **Distinct values** for low-cardinality columns (categories, statuses, names, payment methods, etc.)
  — scan the first 100–200 rows to identify them
- **Date range** if a date column is present
- **Key entities** — what are the main dimensions? (products, customers, stores, regions, etc.)
- **Key measures** — what numeric columns exist? (revenue, profit, quantity, cost, margin, etc.)

Note any obvious **data quality issues** visible in the sample:
- Missing or null values in key columns
- Duplicate IDs
- Negative values in quantity/amount columns
- Apparent typos in category names

---

## Step 2 — Design the query catalog

Based on the columns and data discovered in Step 1, design a comprehensive set of SQL query
titles organised into thematic sections. Aim for 40–60 query titles total.

Always include these standard sections if supported by the data:

1. **Revenue & Sales** — totals, breakdowns by each dimension, averages
2. **Volume & Orders** — counts of transactions, units, averages
3. **Profit & Margin** — profit totals, margins, rankings
4. **Customer Analysis** — top customers, frequency, lifetime value (if customer data present)
5. **Product Analysis** — bestsellers, share of total, unit economics (if product data present)
6. **[Entity] Analysis** — one section per additional key entity (store, region, channel, etc.)
7. **Time-Based Analysis** — trends, period comparisons, seasonality (if date column present)
8. **[Category] Analysis** — one section per categorical dimension (payment method, status, etc.)
9. **Data Quality Checks** — queries targeting the specific issues spotted in Step 1

**Mandatory ranking queries** — always generate these if the relevant columns exist. Users
frequently ask natural-language questions like "which product has the highest sales?" and
the answer must be findable in the catalog:

- For every key dimension (product, customer, store, region, etc.):
  - **[Dimension] Ranked by Total Revenue** — `SUM(revenue_col)` per dimension, DESC
  - **[Dimension] Ranked by Total Profit** — `SUM(profit_col)` per dimension, DESC
  - **[Dimension] Ranked by Total Units Sold** — `SUM(quantity_col)` per dimension, DESC
- Each ranking query must include supporting columns (transaction count, revenue, profit,
  avg margin) so a single query answers the full picture, not just one metric.

Tailor section names and query titles to the actual column names and entities in this dataset.
Do not use generic placeholder names — use the real product names, store names, etc. where helpful.

---

## Step 3 — Write `sql_title.md`

Save the catalog to:

```
output/sql/sql_title.md
```

### Entry format

Each query title must be followed immediately by a description on the same line, separated
by ` — ` (space–em-dash–space):

```
N. <Query title> — <Description>
```

**Description rules** (these flow directly into `/sql-create` as the `**Description:**` field):
- One sentence, max 20 words
- Start with a verb: `Shows`, `Returns`, `Ranks`, `Identifies`, `Compares`, `Flags`, `Lists`
- Name the specific metric **and** dimension — not just "revenue" but "total revenue per product"
- Be distinct enough that Claude can select the right query from a user's natural-language question

Good examples:
```
1. Total Sales Revenue — Shows the combined sum of all order revenue across the entire dataset.
2. Total Revenue by Product — Ranks each product by total revenue generated, highest first.
3. Duplicate Order IDs — Flags any order_id that appears more than once in the dataset.
4. Average Unit Price vs Unit Cost by Product — Compares average selling price against cost to show per-product unit margin.
```

### Full file structure

```markdown
# SQL Query Catalog — <csv_filename>

Dataset: `<CSV_FILE>`
Columns: `col1`, `col2`, `col3`, ...

---

## 1. <Section Name>

1. <Query title> — <Description>
2. <Query title> — <Description>
...

---

## 2. <Section Name>

N. <Query title> — <Description>
...

---

*Generated from dataset inspection — <brief one-line summary of dataset scope>*
```

Number queries **continuously** across all sections (do not restart at 1 per section).

---

## Step 4 — Confirm

Tell the user:
- Total number of query titles written
- Sections included
- Path to the output file (`output/sql/sql_title.md`)
- Any data quality issues spotted during inspection
