# Technical Spec — Retail Orders EDA

**Plan source:** `_plans/kaggle_plan.md`
**Dataset(s):** `data/data.csv`
**Output directory:** `output/PROJECT_01/`
**Date:** 2026-04-16

---

## 1. Overview

Four sequential Python scripts perform a fully exploratory analysis of a retail orders dataset. Phase 1 validates data integrity, detects dirty rows, and produces summary statistics. Phase 2 produces univariate distribution and frequency charts. Phase 3 produces bivariate revenue analysis, cross-dimensional breakdowns, a correlation heatmap, and scatter plots. Phase 4 assembles every output into a single self-contained HTML report with base64-embedded images and inline CSS.

---

## 2. Environment

- Python **3.12** via `uv`
- Run commands: `uv run python src/<script>.py`
- Add dependencies: `uv add <package>`

**Dependencies:**
```
pandas
matplotlib
seaborn
scipy
jinja2
```

**Global constants (defined at the top of every script):**
```python
RANDOM_SEED = 42
OUTPUT_DIR  = "output/PROJECT_01"
DATA_PATH   = "data/data.csv"
```

---

## 3. Script Architecture

| Script | Location | Responsibility | Primary Outputs |
|---|---|---|---|
| `phase1_clean.py` | `src/` | Load, validate schema, detect dirty rows, produce summary stats | `dirty.csv`, `summary_stats.csv` |
| `phase2_univariate.py` | `src/` | Numeric distributions; categorical frequency and revenue bar charts | `uni_*.png` |
| `phase3_bivariate.py` | `src/` | Revenue cross-analysis, scatter plots, correlation heatmap, product × city matrix | `bi_*.png` |
| `phase4_report.py` | `src/` | Assemble all outputs into a self-contained HTML report | `report.html` |

All scripts are **independently runnable** in phase order.

---

## 4. Data Contract

### 4.1 Input Schema — `data/data.csv`

| Column | dtype | Expected Values | Nullable |
|---|---|---|---|
| `order_id` | str | Unique, format `ORD###` | No |
| `product` | str | Non-empty string | No |
| `category` | str | Non-empty string | No |
| `city` | str | Non-empty string | No |
| `quantity` | int | > 0 | No |
| `unit_price` | float | > 0.0 | No |
| `total_price` | float | Must equal `round(quantity × unit_price, 2)` | No |

### 4.2 Dirty-Row Rules

Rows are **flagged and excluded from analysis**, not deleted from the source CSV. All flagged rows are written to `output/PROJECT_01/dirty.csv` with a `reason` column (plain-English string). A single row may accumulate multiple reasons joined by `"; "`.

| Rule | Reason string |
|---|---|
| Any column is NULL or empty string | `"null or empty value in <col>"` |
| `quantity` <= 0 | `"quantity must be positive"` |
| `unit_price` <= 0 | `"unit_price must be positive"` |
| `total_price` <= 0 | `"total_price must be positive"` |
| `abs(total_price - quantity × unit_price) > 0.01` | `"total_price inconsistent with quantity × unit_price (diff: <X>)"` |
| Duplicate `order_id` | `"duplicate order_id"` — keep first occurrence, flag subsequent rows |

### 4.3 Clean DataFrame Contract

Subsequent phases load `data/data.csv` and exclude any rows whose `order_id` appears in `dirty.csv`. If `dirty.csv` does not exist (Phase 1 not yet run), log a warning and proceed with all rows.

**Re-apply exclusion pattern at the top of phases 2–4:**
```python
# Load raw data
df = pd.read_csv(DATA_PATH)
# Exclude dirty rows if dirty.csv exists
dirty_path = os.path.join(OUTPUT_DIR, "dirty.csv")
if os.path.exists(dirty_path):
    dirty_ids = pd.read_csv(dirty_path)["order_id"].tolist()
    df = df[~df["order_id"].isin(dirty_ids)]
```

### 4.4 Output File Registry

| File | Phase | Description |
|---|---|---|
| `output/PROJECT_01/dirty.csv` | 1 | Flagged rows with `reason` column |
| `output/PROJECT_01/summary_stats.csv` | 1 | Per-column descriptive statistics |
| `output/PROJECT_01/uni_numeric_distributions.png` | 2 | 1×3 grid: histograms + KDE for quantity, unit_price, total_price |
| `output/PROJECT_01/uni_product_orders.png` | 2 | Order count per product (horizontal bar, sorted) |
| `output/PROJECT_01/uni_category_orders.png` | 2 | Order count per category (bar chart) |
| `output/PROJECT_01/uni_city_orders.png` | 2 | Order count per city (horizontal bar, sorted) |
| `output/PROJECT_01/uni_revenue_by_product.png` | 2 | Total revenue per product (horizontal bar, sorted) |
| `output/PROJECT_01/uni_revenue_by_category.png` | 2 | Total revenue per category (bar chart) |
| `output/PROJECT_01/uni_revenue_by_city.png` | 2 | Total revenue per city (horizontal bar, sorted) |
| `output/PROJECT_01/uni_unit_price_by_product.png` | 2 | Unit price per product — pricing tier bar chart |
| `output/PROJECT_01/bi_revenue_category_grouped.png` | 3 | Grouped bar: total revenue and total quantity per category |
| `output/PROJECT_01/bi_avg_order_value_by_category.png` | 3 | Average total_price per category (bar chart) |
| `output/PROJECT_01/bi_product_city_heatmap.png` | 3 | Heatmap of SUM(total_price) per product × city |
| `output/PROJECT_01/bi_category_city_stacked.png` | 3 | Revenue stacked bar by city, split by category |
| `output/PROJECT_01/bi_quantity_vs_total_price.png` | 3 | Scatter: quantity vs. total_price, coloured by category |
| `output/PROJECT_01/bi_unit_price_vs_total_price.png` | 3 | Scatter: unit_price vs. total_price, coloured by product |
| `output/PROJECT_01/bi_correlation_heatmap.png` | 3 | Pearson correlation matrix: quantity, unit_price, total_price |
| `output/PROJECT_01/report.html` | 4 | Self-contained HTML report with all findings |

---

## 5. Phase Specs

---

### Phase 1 — Data Quality & Cleaning (`src/phase1_clean.py`)

**Inputs:** `data/data.csv`
**Outputs:** `output/PROJECT_01/dirty.csv`, `output/PROJECT_01/summary_stats.csv`

**Steps:**

1. **Setup:** Create `output/PROJECT_01/` if it does not exist.

2. **Load:** Read `data/data.csv`. Assert all 7 columns (`order_id`, `product`, `category`, `city`, `quantity`, `unit_price`, `total_price`) are present; raise `ValueError` naming any missing column.

3. **Type coercion:** Cast `quantity` to `int64`; cast `unit_price` and `total_price` to `float64`. Log a warning (do not raise) if any cast produces NaN.

4. **Dirty-row detection:** Apply each rule from §4.2. Build a dict mapping `order_id` → list of reason strings. Produce a dirty DataFrame with original columns plus a `reason` column. Write to `dirty.csv`.

5. **Additional quality checks (print to stdout, do not flag as dirty):**
   - Products with more than one distinct `unit_price` — print a table of `product`, `price_values`.
   - Products appearing in more than one `category` — print a table of `product`, `categories`.

6. **Summary statistics — numeric columns (`quantity`, `unit_price`, `total_price`):** For each, compute: `count`, `mean`, `std`, `min`, `p25`, `p50`, `p75`, `max`. Save to `summary_stats.csv`.

7. **Summary statistics — categorical columns (`product`, `category`, `city`):** For each, compute value counts and percentage share. Append to `summary_stats.csv` with `N/A` for numeric-only fields.

8. **Print to stdout:** Shape, dirty row count, clean row count, and total revenue (clean rows only).

---

### Phase 2 — Univariate Analysis (`src/phase2_univariate.py`)

**Inputs:** `data/data.csv`, `output/PROJECT_01/dirty.csv`
**Outputs:** 8 PNG files (see §4.4 `uni_*`)

**Plotting style:** Use `seaborn.set_theme(style="whitegrid", context="notebook")` globally. Figure DPI = 150. All axes must have a title, labelled x-axis, labelled y-axis. Save with `bbox_inches="tight"`.

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3).

2. **Numeric distributions** (`uni_numeric_distributions.png`):
   - 1×3 subplot grid for `quantity`, `unit_price`, `total_price`.
   - Each subplot: histogram (bins=20, alpha=0.6) + KDE overlay.
   - Annotate mean with a dashed vertical line and median with a dotted line; label each.
   - Super-title: `"Numeric Column Distributions"`.

3. **Product order count** (`uni_product_orders.png`):
   - Horizontal bar chart, sorted descending by count.
   - Title: `"Orders per Product"`. Annotate count on each bar.

4. **Category order count** (`uni_category_orders.png`):
   - Vertical bar chart. Title: `"Orders per Category"`. Annotate count on each bar.

5. **City order count** (`uni_city_orders.png`):
   - Horizontal bar chart, sorted descending. Title: `"Orders per City"`. Annotate count.

6. **Revenue per product** (`uni_revenue_by_product.png`):
   - Horizontal bar chart sorted descending by `SUM(total_price)`.
   - Annotate revenue value on each bar (formatted as currency: `£{value:,.2f}`).
   - Title: `"Total Revenue by Product"`.

7. **Revenue per category** (`uni_revenue_by_category.png`):
   - Vertical bar chart. Annotate revenue on each bar. Title: `"Total Revenue by Category"`.

8. **Revenue per city** (`uni_revenue_by_city.png`):
   - Horizontal bar chart sorted descending. Annotate revenue. Title: `"Total Revenue by City"`.

9. **Unit price by product** (`uni_unit_price_by_product.png`):
   - Vertical bar chart sorted descending by `unit_price`. Annotate price on each bar.
   - Title: `"Unit Price by Product"`. Use a contrasting colour to distinguish from revenue charts.

---

### Phase 3 — Bivariate & Revenue Analysis (`src/phase3_bivariate.py`)

**Inputs:** `data/data.csv`, `output/PROJECT_01/dirty.csv`
**Outputs:** 7 PNG files (see §4.4 `bi_*`)

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3).

2. **Revenue and quantity by category — grouped bar** (`bi_revenue_category_grouped.png`):
   - Two grouped bars per category: one for `SUM(total_price)`, one for `SUM(quantity)`.
   - Use a secondary y-axis for quantity (scale differs significantly from revenue).
   - Title: `"Revenue and Quantity by Category"`. Legend distinguishes the two metrics.

3. **Average order value by category** (`bi_avg_order_value_by_category.png`):
   - Bar chart of `MEAN(total_price)` per category. Annotate value on each bar.
   - Title: `"Average Order Value by Category"`.

4. **Product × city revenue heatmap** (`bi_product_city_heatmap.png`):
   - Pivot table: `index=product`, `columns=city`, `values=total_price`, `aggfunc=sum`. Fill NaN with 0.
   - Seaborn heatmap with `annot=True`, `fmt=".0f"`, `cmap="YlOrRd"`.
   - Title: `"Revenue Heatmap: Product × City"`.

5. **Category × city stacked revenue bar** (`bi_category_city_stacked.png`):
   - Stacked bar chart: x = `city`, stacks = `category`, y = `SUM(total_price)`.
   - Annotate each segment with its value. Legend for category.
   - Title: `"Revenue by City, Split by Category"`.

6. **Scatter: quantity vs. total_price** (`bi_quantity_vs_total_price.png`):
   - Scatter plot coloured by `category` (qualitative palette).
   - Annotate each point with `product` name (offset slightly).
   - Add a linear regression line using `seaborn.regplot` (without CI band for clarity).
   - Title: `"Quantity vs. Total Price (coloured by Category)"`.
   - Add a note in the subtitle: `"Note: total_price = quantity × unit_price (derived relationship)"`.

7. **Scatter: unit_price vs. total_price** (`bi_unit_price_vs_total_price.png`):
   - Scatter plot coloured by `product`.
   - Annotate each point with the `city` of the order.
   - Title: `"Unit Price vs. Total Price (coloured by Product)"`.

8. **Correlation heatmap** (`bi_correlation_heatmap.png`):
   - Pearson correlation matrix for `quantity`, `unit_price`, `total_price`.
   - Lower-triangle seaborn heatmap: `annot=True`, `fmt=".2f"`, `vmin=-1`, `vmax=1`, `cmap="coolwarm"`.
   - Title: `"Pearson Correlation — Numeric Columns"`.
   - Add a note below the figure: `"total_price is derived from quantity × unit_price; interpret correlations accordingly."`.

---

### Phase 4 — HTML Report (`src/phase4_report.py`)

**Inputs:** all files in `output/PROJECT_01/` (PNGs and CSVs from phases 1–3)
**Outputs:** `output/PROJECT_01/report.html`

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3 — for inline statistics in the executive summary).

2. **Load all artefacts:**
   - Read `summary_stats.csv`, `dirty.csv` into DataFrames.
   - Collect all PNG files into a dict keyed by filename stem.
   - Encode each PNG as a base64 data URI.

3. **Compute inline statistics for executive summary:**
   - `n_total`, `n_dirty`, `n_clean`.
   - Total revenue (sum of `total_price`).
   - Top product by revenue and by quantity.
   - Top category by revenue.
   - Top city by revenue.
   - Mean and median `total_price`.
   - Whether any data quality issues were found (dirty row count).

4. **HTML structure** — single file with inline `<style>`:
   - `<head>`: UTF-8 charset, viewport meta, inline CSS (white background, max-width 1100px centred, `font-family: "Segoe UI", sans-serif`, table borders, section headers).
   - Jump links at the top for each section.
   - **Section 1 — Executive Summary:** 4–6 bullet points of key revenue and data quality findings from inline statistics.
   - **Section 2 — Dataset Overview:** Rendered HTML table from `summary_stats.csv`. Note the current row count and flag if only a sample is loaded.
   - **Section 3 — Data Quality:** Count of dirty rows. Rendered table of `dirty.csv` rows (or `"No data quality issues detected."` if clean). Include derived-column consistency check results.
   - **Section 4 — Univariate Analysis:** All `uni_*.png` images in order, each `width="100%"` with a caption.
   - **Section 5 — Revenue & Bivariate Analysis:** All `bi_*.png` images in order with captions. After the correlation heatmap, include an HTML callout box explaining the derived column caveat.
   - **Section 6 — Interview Preparation Notes:** A static HTML block with 8–10 bullet points covering:
     - Revenue vs. volume distinction (why total_price ≠ profitability).
     - The derived column trap and its effect on correlation interpretation.
     - When to use mean vs. median for price analysis.
     - How to approach categorical aggregation choices (sum vs. mean vs. count).
     - Why the absence of a date column limits the analysis.
     - What a price consistency check reveals about discounting or data entry errors.
     - How to interpret a product × city heatmap for sales strategy.
     - Data quality dimensions: completeness, consistency, validity, uniqueness.
   - Footer: `"Generated by Claude Code — Project 01 — 2026-04-16"`.

5. Write the complete HTML to `output/PROJECT_01/report.html`.

6. Print to stdout: `"Report saved to output/PROJECT_01/report.html"` and file size in KB.

---

## 6. Reproducibility

All scripts independently runnable in phase order:

```bash
uv run python src/phase1_clean.py
uv run python src/phase2_univariate.py
uv run python src/phase3_bivariate.py
uv run python src/phase4_report.py
```

Phases 2–4 re-apply dirty-row exclusion on each run — no intermediate cleaned CSV is persisted.

---

## 7. Error Handling

| Condition | Behaviour |
|---|---|
| `data/data.csv` not found | Raise `FileNotFoundError("data/data.csv not found — place dataset in data/ directory")` |
| Expected column missing from CSV | Raise `ValueError("Missing required column: <col_name>")` |
| `dirty.csv` not found when running phases 2–4 | Log a `warnings.warn` — proceed with full dataset |
| PNG file missing when building report | Log a warning, skip that image, insert `<p>[image not generated]</p>` placeholder |
| Type coercion produces NaN | Log `warnings.warn` — do not raise; include in dirty row detection |

---

## 8. Plot Style Standards

Applied consistently across all scripts:

- `seaborn.set_theme(style="whitegrid", context="notebook")`
- Figure DPI: `150`
- Save: `fig.savefig(path, dpi=150, bbox_inches="tight")`
- Close after saving: `plt.close(fig)` — prevents memory accumulation
- Revenue colour: `"#2563eb"` (blue)
- Quantity colour: `"#16a34a"` (green)
- Category palette: qualitative (seaborn `"Set2"`)
- Product palette: qualitative (seaborn `"tab10"`)
- All titles in title case. All axis labels in sentence case.
- Currency formatting: `f"£{value:,.2f}"` on all revenue annotations.
