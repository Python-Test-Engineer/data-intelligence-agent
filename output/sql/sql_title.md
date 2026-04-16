# SQL Query Catalog — data.csv

Dataset: `C:\Users\mrcra\Desktop\data-intelligence-agent\data\data.csv`
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

12. date Ranked by Total quantity — Ranks each date by total quantity, highest first.
13. product_name Ranked by Total quantity — Ranks each product_name by total quantity, highest first.
14. city Ranked by Total quantity — Ranks each city by total quantity, highest first.

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
23. Performance Summary for a Specific date — Returns transaction count and all key metrics for a single date value.
24. product_name Breakdown for date = :date — Ranks each product_name by total unit_price filtered to a single date value.
25. city Breakdown for date = :date — Ranks each city by total unit_price filtered to a single date value.
26. Filter by product_name — Returns all rows where product_name matches a given value.
27. Performance Summary for a Specific product_name — Returns transaction count and all key metrics for a single product_name value.
28. date Breakdown for product_name = :product_name — Ranks each date by total unit_price filtered to a single product_name value.
29. city Breakdown for product_name = :product_name — Ranks each city by total unit_price filtered to a single product_name value.
30. Filter by city — Returns all rows where city matches a given value.
31. Performance Summary for a Specific city — Returns transaction count and all key metrics for a single city value.
32. date Breakdown for city = :city — Ranks each date by total unit_price filtered to a single city value.
33. product_name Breakdown for city = :city — Ranks each product_name by total unit_price filtered to a single city value.
34. Rows Where unit_price Exceeds :min_value — Returns all rows where unit_price is above a given threshold.
35. date with Total unit_price Above :threshold — Lists date values whose total unit_price exceeds a given threshold.

---

## Data Quality Checks

36. Missing Values per Column — Counts NULL values in each column to identify data gaps.
37. Duplicate order_id Values — Flags any order_id that appears more than once in the dataset.
38. Negative unit_price Values — Flags rows where unit_price is negative, which may indicate data errors.
39. Negative quantity Values — Flags rows where quantity is negative, which may indicate data errors.
40. Negative total_price Values — Flags rows where total_price is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (20 rows, 7 columns)*