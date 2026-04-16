# Research Plan — Retail Orders Exploratory Analysis

**Idea source:** `_ideas/kaggle_ideas.md`
**Dataset(s):** `data/data.csv`
**Date:** 2026-04-16

---

## 1. Research Question

Perform a thorough exploratory data analysis (EDA) of a retail orders dataset containing order identifiers, product and category dimensions, a geographic (city) dimension, and three revenue-related numeric columns (quantity, unit price, total price). The goal is to uncover sales patterns, product and category performance, geographic revenue distribution, pricing structure, and data quality issues — preparing for interview questions ranging from basic descriptive statistics to advanced analytical reasoning.

---

## 2. Dataset Summary

| Column | Type | Notes |
|---|---|---|
| `order_id` | Categorical (ID) | Unique per row — primary key; format `ORD###` |
| `product` | Categorical | Product name (e.g. Monitor, Mouse, Keyboard) |
| `category` | Categorical | Product category (e.g. Electronics, Accessories) |
| `city` | Categorical | City of the order (e.g. New York, London, Paris) |
| `quantity` | Numeric (int) | Units ordered — must be positive |
| `unit_price` | Numeric (float) | Price per unit — must be positive |
| `total_price` | Numeric (float) | Derived: `quantity × unit_price` — must equal the product of the two |

### Key Observations from Sample

- **`total_price` is a derived column** — it must always equal `quantity × unit_price`. Any deviation signals a data quality issue.
- **No date column** — time-series and trend analysis are not possible with the current schema. This is a notable analytical gap.
- **Three categorical dimensions** (`product`, `category`, `city`) allow multi-dimensional revenue slicing.
- **`order_id`** is an identifier and must be excluded from all aggregations.
- **`unit_price` is a list/sale price** — profit margin analysis is not possible without a cost column.
- **Accessories dominates by order count** (2 of 3 rows); Electronics leads revenue (Monitor at £3,499.90 vs £789.87 for Accessories combined).

---

## 3. Proposed Phases

### Phase 1 — Data Quality & Cleaning
- **Schema validation:** Confirm all 7 expected columns are present with correct types.
- **Dirty row detection:**
  - NULL or empty values in any column
  - Duplicate `order_id` values (flag subsequent occurrences as duplicates)
  - Negative or zero `quantity`, `unit_price`, or `total_price`
  - `total_price` inconsistent with `round(quantity × unit_price, 2)` — flag any discrepancy > £0.01
  - Products appearing in more than one category (category-product mapping inconsistency)
- **Summary statistics:** Descriptive table for numeric columns (count, mean, std, min, Q25, Q50, Q75, max); value counts and percentages for categorical columns.
- **Output:** `output/PROJECT_01/dirty.csv` with `reason` column; `output/PROJECT_01/summary_stats.csv`.

### Phase 2 — Univariate Analysis
- **Numeric distributions:** Histograms with KDE overlay for `quantity`, `unit_price`, `total_price`.
  - Annotate mean and median with vertical lines on each plot.
  - Note any visible skew (expected: `unit_price` and `total_price` right-skewed if full dataset has many low-price accessories alongside a few high-price electronics items).
- **Categorical frequency charts:**
  - Bar chart: order count per `product` (horizontal, sorted descending).
  - Bar chart: order count per `category`.
  - Bar chart: order count per `city`.
- **Revenue bar charts (per dimension):**
  - Total `total_price` per `product` — ranked descending.
  - Total `total_price` per `category`.
  - Total `total_price` per `city`.
- **Price-point chart:** `unit_price` per product — reveals product pricing tiers clearly.

### Phase 3 — Bivariate & Revenue Analysis
- **Revenue by category:** Side-by-side grouped bar: total revenue and total quantity per `category`.
- **Revenue by product:** Ranked horizontal bar of `total_price` per product — top revenue contributors.
- **Revenue by city:** Ranked horizontal bar of `total_price` per city — geographic revenue split.
- **Average order value by category:** `AVG(total_price)` grouped by category — distinguishes price-driven vs. volume-driven categories.
- **Product × city revenue heatmap:** Grid heatmap of `SUM(total_price)` for each product × city combination — identifies geographic concentration per product.
- **Category × city stacked bar:** Revenue stacked by category per city.
- **Quantity vs. total price scatter:** Scatter plot coloured by `category` — confirms the `total_price = quantity × unit_price` relationship and reveals any outliers.
- **Unit price vs. total price scatter:** Scatter coloured by `product` — checks within-product pricing consistency across orders.
- **Correlation heatmap:** Pearson correlations for `quantity`, `unit_price`, `total_price`. Note: the high `unit_price`–`total_price` correlation is partially mathematical; the `quantity`–`total_price` relationship is the more analytically meaningful signal.

### Phase 4 — Data Quality Deep-Dive
- **Derived column audit:** Verify `total_price == round(quantity × unit_price, 2)` row by row; produce a table of discrepancies.
- **Price consistency check:** Flag any product with more than one distinct `unit_price` across rows — suggests pricing inconsistency or promotional pricing.
- **Category–product mapping audit:** Confirm each product maps to exactly one category; flag exceptions.
- **Order ID uniqueness audit:** Confirm no duplicate `order_id`; assess whether the ID format (`ORD###`) is sequential and gap-free.

### Phase 5 — Reporting
- **HTML report** — a single self-contained file consolidating:
  - Executive summary (key revenue figures, top product/category/city, data quality status).
  - All charts embedded as base64 PNGs.
  - Summary statistics tables.
  - Data quality findings table.
  - Interview preparation notes (see Section 5 below).
- Save to `output/PROJECT_01/report.html`.

---

## 4. Technical Spec Guidance

The `/spec` phase should produce the following scripts:

| Script | Phase | Purpose | Key Outputs |
|---|---|---|---|
| `phase1_clean.py` | 1 | Load CSV, validate schema, detect dirty rows, produce summary stats | `dirty.csv`, `summary_stats.csv` |
| `phase2_univariate.py` | 2 | Distribution plots for numerics; frequency and revenue bar charts for categoricals | `uni_*.png` |
| `phase3_bivariate.py` | 3 | Revenue cross-analysis, correlation heatmap, scatter plots, heatmap matrix | `bi_*.png` |
| `phase4_report.py` | 4 | Assemble all outputs into a single self-contained HTML report | `report.html` |

### Data Contracts Between Scripts
- All scripts read from `data/data.csv` directly; Phases 2–4 re-apply dirty-row exclusion from `dirty.csv` on each run (if the file exists).
- All PNGs saved to `output/PROJECT_01/` with `uni_` or `bi_` prefix.
- Phase 4 reads all PNGs and CSVs from `output/PROJECT_01/` to assemble the HTML.
- `RANDOM_SEED = 42` and `OUTPUT_DIR = "output/PROJECT_01"` defined at the top of every script.

### Libraries
- **pandas** — data manipulation and aggregation
- **matplotlib + seaborn** — all static charts and heatmaps
- **scipy.stats** — Pearson correlation, descriptive stats
- **jinja2** or f-string templating — HTML report assembly

---

## 5. Interview Preparation Notes

Key analytical topics this dataset is likely to probe:

- **Revenue vs. volume distinction:** Total price measures revenue; quantity measures volume. A high-revenue product may have low volume (high unit price) or high volume (low unit price). Monitor is the clearest example — one order, highest revenue.
- **Derived column trap:** `total_price = quantity × unit_price` is a mathematical identity, not an independent measurement. Correlation between these columns is partially spurious — always acknowledge this.
- **Categorical aggregation choices:** Mean vs. sum vs. count tell very different stories per category. Know which to use and why.
- **Missing date dimension:** Without a date field, no trend, seasonality, or cohort analysis is possible. This is a data gap worth raising proactively.
- **Single-row-per-product limitation (in sample):** With one row per product in the sample, averages equal individual values — be careful not to over-interpret sample statistics.
- **Geographic analysis caveats:** City-level data may reflect market size, sales rep performance, or regional pricing — without additional context these are indistinguishable.
- **Data quality rigour:** Ability to spot the derived column inconsistency check and price consistency check demonstrates analytical thoroughness beyond simple EDA.

---

## 6. Open Questions

1. **Dataset size:** The current `data/data.csv` contains 3 rows. Is this a sample, or the full dataset? If larger, does it include a date column?
2. **Order granularity:** Does one row represent a single order line (one product per row), or a complete order? If line-level, `order_id` may not be unique in the full dataset.
3. **Currency:** Are all prices in a single currency, or do city rows reflect different currencies requiring normalisation?
4. **Cost data:** Is a cost price or margin column available in the full dataset, or is analysis constrained to revenue and volume?
5. **Interview focus:** Are there specific analytical angles to prepare for — e.g. pricing strategy, geographic performance, category mix?

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Only 3 rows in sample | Cannot derive meaningful distributions or rankings | Proceed with schema-level analysis; note all findings are illustrative pending full data load |
| No date column | No trend or time-based analysis | Flag as gap; recommend requesting a date-enriched version of the dataset |
| `total_price` is derived | High correlation with `unit_price` is mathematical, not behavioural | Label clearly in all correlation commentary |
| No cost data | Cannot assess profitability | Distinguish revenue from profit in all commentary |
| Single city per order (assumed) | If orders are multi-city (e.g. split shipments), city aggregations are misleading | Phase 1 validation will confirm order_id × city uniqueness |
