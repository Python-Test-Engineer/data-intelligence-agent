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
6. Total unit_price by product_name — Ranks each product_name by total unit_price, highest first.
7. Average unit_price by product_name — Compares average unit_price across each product_name.
8. Total quantity by product_name — Ranks each product_name by total quantity, highest first.

---

## Categorical Distributions

9. Distribution of product_name — Counts rows for each distinct value of product_name, ordered by frequency.
10. Distribution of city — Counts rows for each distinct value of city, ordered by frequency.

---

## Rankings

11. Top 10 product_name by unit_price — Lists the 10 product_name values with the highest total unit_price.
12. Bottom 10 product_name by unit_price — Lists the 10 product_name values with the lowest total unit_price.
13. Top 10 city by unit_price — Lists the 10 city values with the highest total unit_price.

---

## Multi-Dimensional

14. unit_price by product_name and city — Shows total unit_price broken down by both product_name and city.

---

## Parametric Lookups

15. Filter by product_name — Returns all rows where product_name matches a given value.
16. Total unit_price for a Specific product_name — Returns total unit_price for a single product_name value.

---

## Time-Based Analysis

17. Monthly unit_price Trend — Returns total unit_price grouped by year and month.
18. Yearly unit_price Total — Returns total unit_price grouped by year.
19. Date Range Filter — Returns rows between a start and end date for date.

---

## Data Quality Checks

20. Missing Values per Column — Counts NULL values in each column to identify data gaps.
21. Duplicate order_id Values — Flags any order_id that appears more than once in the dataset.
22. Negative unit_price Values — Flags rows where unit_price is negative, which may indicate data errors.
23. Negative quantity Values — Flags rows where quantity is negative, which may indicate data errors.
24. Negative total_price Values — Flags rows where total_price is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (20 rows, 7 columns)*