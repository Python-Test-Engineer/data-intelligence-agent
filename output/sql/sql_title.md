# SQL Query Catalog — data.csv

Dataset: `data\data.csv`
Columns: `order_id`, `date`, `customer_id`, `customer_name`, `product_id`, `product_name`, `unit_price`, `quantity`, `total_price`, `store_id`, `store_name`, `city`, `payment_method`

---

## Overview

1. Row Count — Returns the total number of rows in the dataset.
2. Column Sample — Returns the first 10 rows to preview the dataset structure.

---

## Numeric Summaries

3. Summary Stats for unit_price — Returns min, max, average, and total for unit_price.
4. Summary Stats for quantity — Returns min, max, average, and total for quantity.
5. Summary Stats for total_price — Returns min, max, average, and total for total_price.
6. Total unit_price by customer_name — Ranks each customer_name by total unit_price, highest first.
7. Average unit_price by customer_name — Compares average unit_price across each customer_name.
8. Total quantity by customer_name — Ranks each customer_name by total quantity, highest first.

---

## Categorical Distributions

9. Distribution of customer_name — Counts rows for each distinct value of customer_name, ordered by frequency.
10. Distribution of product_name — Counts rows for each distinct value of product_name, ordered by frequency.
11. Distribution of store_name — Counts rows for each distinct value of store_name, ordered by frequency.
12. Distribution of city — Counts rows for each distinct value of city, ordered by frequency.
13. Distribution of payment_method — Counts rows for each distinct value of payment_method, ordered by frequency.

---

## Rankings

14. Top 10 customer_name by unit_price — Lists the 10 customer_name values with the highest total unit_price.
15. Bottom 10 customer_name by unit_price — Lists the 10 customer_name values with the lowest total unit_price.
16. Top 10 product_name by unit_price — Lists the 10 product_name values with the highest total unit_price.

---

## Multi-Dimensional

17. unit_price by customer_name and product_name — Shows total unit_price broken down by both customer_name and product_name.

---

## Parametric Lookups

18. Filter by customer_name — Returns all rows where customer_name matches a given value.
19. Total unit_price for a Specific customer_name — Returns total unit_price for a single customer_name value.

---

## Time-Based Analysis

20. Monthly unit_price Trend — Returns total unit_price grouped by year and month.
21. Yearly unit_price Total — Returns total unit_price grouped by year.
22. Date Range Filter — Returns rows between a start and end date for date.

---

## Data Quality Checks

23. Missing Values per Column — Counts NULL values in each column to identify data gaps.
24. Duplicate order_id Values — Flags any order_id that appears more than once in the dataset.
25. Negative unit_price Values — Flags rows where unit_price is negative, which may indicate data errors.
26. Negative quantity Values — Flags rows where quantity is negative, which may indicate data errors.
27. Negative total_price Values — Flags rows where total_price is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (50 rows, 13 columns)*