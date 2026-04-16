# SQL Query Catalog — test_data.csv

Dataset: `C:\Users\mrcra\AppData\Local\Temp\pytest-of-mrcra\pytest-30\test_run_tests_and_merge_inlin0\test_data.csv`
Columns: `product`, `quantity`, `price`

---

## Overview

1. Row Count — Returns the total number of rows in the dataset.
2. Column Sample — Returns the first 10 rows to preview the dataset structure.

---

## Numeric Summaries

3. Summary Stats for quantity — Returns min, max, average, and total for quantity.
4. Summary Stats for price — Returns min, max, average, and total for price.
5. Total quantity by product — Ranks each product by total quantity, highest first.
6. Average quantity by product — Compares average quantity across each product.
7. Total price by product — Ranks each product by total price, highest first.

---

## Categorical Distributions

8. Distribution of product — Counts rows for each distinct value of product, ordered by frequency.

---

## Rankings

9. product Ranked by Total quantity — Ranks each product by total quantity, highest first.

---

## Multi-Metric Analysis

10. Performance Breakdown by product — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by product.

---

## Parametric Lookups

11. Filter by product — Returns all rows where product matches a given value.
12. Performance Summary for a Specific product — Returns transaction count and all key metrics for a single product value.
13. Rows Where quantity Exceeds :min_value — Returns all rows where quantity is above a given threshold.
14. product with Total quantity Above :threshold — Lists product values whose total quantity exceeds a given threshold.

---

## Data Quality Checks

15. Missing Values per Column — Counts NULL values in each column to identify data gaps.
16. Negative quantity Values — Flags rows where quantity is negative, which may indicate data errors.
17. Negative price Values — Flags rows where price is negative, which may indicate data errors.

---

*Generated from dataset inspection — test_data.csv (4 rows, 3 columns)*