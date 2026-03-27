# SQL Query Catalog — data.csv

Dataset: `data\data.csv`
Columns: `order_id`, `date`, `product_name`, `unit_price`, `quantity`, `total_price`, `city`

---

## Overview

1. Row Count — Returns the total number of rows in the dataset.
2. Column Sample — Returns the first 10 rows to preview the dataset structure.

---

## Numeric Summaries

3. Summary Stats for unit_price — Returns min, max, average, and total for unit_price.
4. Summary Stats for quantity — Returns min, max, average, and total for quantity.
5. Summary Stats for total_price — Returns min, max, average, and total for total_price.
6. Total unit_price by date — Ranks each date by total unit_price, highest first.
7. Average unit_price by date — Compares average unit_price across each date.
8. Total quantity by date — Ranks each date by total quantity, highest first.

---

## Categorical Distributions

9. Distribution of date — Counts rows for each distinct value of date, ordered by frequency.
10. Distribution of product_name — Counts rows for each distinct value of product_name, ordered by frequency.
11. Distribution of city — Counts rows for each distinct value of city, ordered by frequency.

---

## Rankings

12. Top 10 date by unit_price — Lists the 10 date values with the highest total unit_price.
13. Bottom 10 date by unit_price — Lists the 10 date values with the lowest total unit_price.
14. Top 10 product_name by unit_price — Lists the 10 product_name values with the highest total unit_price.

---

## Multi-Dimensional

15. unit_price by date and product_name — Shows total unit_price broken down by both date and product_name.

---

## Multi-Metric Analysis

16. Performance Breakdown by date — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by date.
17. Performance Breakdown by product_name — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by product_name.
18. Performance Breakdown by city — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by city.
19. date × product_name Performance Matrix — Shows performance metrics for every date and product_name combination, ordered by profitability.
20. Unique order_id Count by date — Counts distinct order_id values and key metrics per date to reveal concentration.
21. Unique order_id Count by product_name — Counts distinct order_id values and key metrics per product_name to reveal concentration.

---

## Parametric Lookups

22. Filter by date — Returns all rows where date matches a given value.
23. Total unit_price for a Specific date — Returns total unit_price for a single date value.

---

## Data Quality Checks

24. Missing Values per Column — Counts NULL values in each column to identify data gaps.
25. Duplicate order_id Values — Flags any order_id that appears more than once in the dataset.
26. Negative unit_price Values — Flags rows where unit_price is negative, which may indicate data errors.
27. Negative quantity Values — Flags rows where quantity is negative, which may indicate data errors.
28. Negative total_price Values — Flags rows where total_price is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (20 rows, 7 columns)*