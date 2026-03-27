# SQL Query Catalog — data.csv

Dataset: `data\data.csv`
Columns: `order_id`, `date`, `customer_id`, `customer_name`, `product_id`, `product_name`, `unit_cost`, `unit_price`, `quantity`, `total_cost`, `total_revenue`, `profit`, `margin_pct`, `store_id`, `store_name`, `city`, `payment_method`

---

## Overview

1. Row Count — Returns the total number of rows in the dataset.
2. Column Sample — Returns the first 10 rows to preview the dataset structure.

---

## Numeric Summaries

3. Summary Stats for unit_cost — Returns min, max, average, and total for unit_cost.
4. Summary Stats for unit_price — Returns min, max, average, and total for unit_price.
5. Summary Stats for quantity — Returns min, max, average, and total for quantity.
6. Summary Stats for total_cost — Returns min, max, average, and total for total_cost.
7. Summary Stats for total_revenue — Returns min, max, average, and total for total_revenue.
8. Summary Stats for profit — Returns min, max, average, and total for profit.
9. Total unit_cost by customer_name — Ranks each customer_name by total unit_cost, highest first.
10. Average unit_cost by customer_name — Compares average unit_cost across each customer_name.
11. Total unit_price by customer_name — Ranks each customer_name by total unit_price, highest first.

---

## Categorical Distributions

12. Distribution of customer_name — Counts rows for each distinct value of customer_name, ordered by frequency.
13. Distribution of product_name — Counts rows for each distinct value of product_name, ordered by frequency.
14. Distribution of store_name — Counts rows for each distinct value of store_name, ordered by frequency.
15. Distribution of city — Counts rows for each distinct value of city, ordered by frequency.
16. Distribution of payment_method — Counts rows for each distinct value of payment_method, ordered by frequency.

---

## Rankings

17. Top 10 customer_name by unit_cost — Lists the 10 customer_name values with the highest total unit_cost.
18. Bottom 10 customer_name by unit_cost — Lists the 10 customer_name values with the lowest total unit_cost.
19. Top 10 product_name by unit_cost — Lists the 10 product_name values with the highest total unit_cost.

---

## Multi-Dimensional

20. unit_cost by customer_name and product_name — Shows total unit_cost broken down by both customer_name and product_name.

---

## Multi-Metric Analysis

21. Performance Breakdown by customer_name — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by customer_name.
22. Performance Breakdown by product_name — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by product_name.
23. Performance Breakdown by store_name — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by store_name.
24. customer_name × product_name Performance Matrix — Shows performance metrics for every customer_name and product_name combination, ordered by profitability.
25. Unique order_id Count by customer_name — Counts distinct order_id values and key metrics per customer_name to reveal concentration.
26. Unique order_id Count by product_name — Counts distinct order_id values and key metrics per product_name to reveal concentration.

---

## Parametric Lookups

27. Filter by customer_name — Returns all rows where customer_name matches a given value.
28. Total unit_cost for a Specific customer_name — Returns total unit_cost for a single customer_name value.

---

## Data Quality Checks

29. Missing Values per Column — Counts NULL values in each column to identify data gaps.
30. Duplicate order_id Values — Flags any order_id that appears more than once in the dataset.
31. Negative unit_cost Values — Flags rows where unit_cost is negative, which may indicate data errors.
32. Negative unit_price Values — Flags rows where unit_price is negative, which may indicate data errors.
33. Negative quantity Values — Flags rows where quantity is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (100 rows, 17 columns)*