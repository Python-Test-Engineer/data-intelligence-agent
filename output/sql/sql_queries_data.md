# SQL Query Catalog
<!-- source: data.csv | table: data | generated: 2026-03-26 | queries: 24 -->

---

### Overview

## Row Count
**ARGS:** —
**Description:** Returns the total number of rows in the dataset.
```sql
SELECT COUNT(*) AS row_count
FROM data;
```
---

## Column Sample
**ARGS:** —
**Description:** Returns the first 10 rows to preview the dataset structure.
```sql
SELECT *
FROM data
LIMIT 10;
```
---

### Numeric Summaries

## Summary Stats for unit_price
**ARGS:** —
**Description:** Returns min, max, average, and total for unit_price.
```sql
SELECT
    MIN(unit_price) AS min_val,
    MAX(unit_price) AS max_val,
    ROUND(AVG(unit_price), 2) AS avg_val,
    SUM(unit_price) AS total
FROM data;
```
---

## Summary Stats for quantity
**ARGS:** —
**Description:** Returns min, max, average, and total for quantity.
```sql
SELECT
    MIN(quantity) AS min_val,
    MAX(quantity) AS max_val,
    ROUND(AVG(quantity), 2) AS avg_val,
    SUM(quantity) AS total
FROM data;
```
---

## Summary Stats for total_price
**ARGS:** —
**Description:** Returns min, max, average, and total for total_price.
```sql
SELECT
    MIN(total_price) AS min_val,
    MAX(total_price) AS max_val,
    ROUND(AVG(total_price), 2) AS avg_val,
    SUM(total_price) AS total
FROM data;
```
---

## Total unit_price by product_name
**ARGS:** —
**Description:** Ranks each product_name by total unit_price, highest first.
```sql
SELECT product_name, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY product_name
ORDER BY total_unit_price DESC;
```
---

## Average unit_price by product_name
**ARGS:** —
**Description:** Compares average unit_price across each product_name.
```sql
SELECT product_name, ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM data
GROUP BY product_name
ORDER BY avg_unit_price DESC;
```
---

## Total quantity by product_name
**ARGS:** —
**Description:** Ranks each product_name by total quantity, highest first.
```sql
SELECT product_name, SUM(quantity) AS total_quantity
FROM data
GROUP BY product_name
ORDER BY total_quantity DESC;
```
---

### Categorical Distributions

## Distribution of product_name
**ARGS:** —
**Description:** Counts rows for each distinct value of product_name, ordered by frequency.
```sql
SELECT product_name, COUNT(*) AS row_count
FROM data
GROUP BY product_name
ORDER BY row_count DESC;
```
---

## Distribution of city
**ARGS:** —
**Description:** Counts rows for each distinct value of city, ordered by frequency.
```sql
SELECT city, COUNT(*) AS row_count
FROM data
GROUP BY city
ORDER BY row_count DESC;
```
---

### Rankings

## Top 10 product_name by unit_price
**ARGS:** —
**Description:** Lists the 10 product_name values with the highest total unit_price.
```sql
SELECT product_name, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY product_name
ORDER BY total_unit_price DESC
LIMIT 10;
```
---

## Bottom 10 product_name by unit_price
**ARGS:** —
**Description:** Lists the 10 product_name values with the lowest total unit_price.
```sql
SELECT product_name, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY product_name
ORDER BY total_unit_price ASC
LIMIT 10;
```
---

## Top 10 city by unit_price
**ARGS:** —
**Description:** Lists the 10 city values with the highest total unit_price.
```sql
SELECT city, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY city
ORDER BY total_unit_price DESC
LIMIT 10;
```
---

### Multi-Dimensional

## unit_price by product_name and city
**ARGS:** —
**Description:** Shows total unit_price broken down by both product_name and city.
```sql
SELECT product_name, city, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY product_name, city
ORDER BY total_unit_price DESC;
```
---

### Parametric Lookups

## Filter by product_name
**ARGS:** product_name
**Description:** Returns all rows where product_name matches a given value.
```sql
SELECT *
FROM data
WHERE product_name = :product_name;
```
---

## Total unit_price for a Specific product_name
**ARGS:** product_name
**Description:** Returns total unit_price for a single product_name value.
```sql
SELECT product_name, SUM(unit_price) AS total_unit_price
FROM data
WHERE product_name = :product_name
GROUP BY product_name;
```
---

### Time-Based Analysis

## Monthly unit_price Trend
**ARGS:** —
**Description:** Returns total unit_price grouped by year and month.
```sql
SELECT
    strftime('%Y-%m', date) AS month,
    SUM(unit_price) AS total_unit_price
FROM data
GROUP BY month
ORDER BY month;
```
---

## Yearly unit_price Total
**ARGS:** —
**Description:** Returns total unit_price grouped by year.
```sql
SELECT
    strftime('%Y', date) AS year,
    SUM(unit_price) AS total_unit_price
FROM data
GROUP BY year
ORDER BY year;
```
---

## Date Range Filter
**ARGS:** start_date, end_date
**Description:** Returns rows between a start and end date for date.
```sql
SELECT *
FROM data
WHERE date BETWEEN :start_date AND :end_date
ORDER BY date;
```
---

### Data Quality Checks

## Missing Values per Column
**ARGS:** —
**Description:** Counts NULL values in each column to identify data gaps.
```sql
SELECT 'order_id' AS column_name, COUNT(*) AS null_count FROM data WHERE order_id IS NULL
UNION ALL
SELECT 'date' AS column_name, COUNT(*) AS null_count FROM data WHERE date IS NULL
UNION ALL
SELECT 'product_name' AS column_name, COUNT(*) AS null_count FROM data WHERE product_name IS NULL
UNION ALL
SELECT 'unit_price' AS column_name, COUNT(*) AS null_count FROM data WHERE unit_price IS NULL
UNION ALL
SELECT 'quantity' AS column_name, COUNT(*) AS null_count FROM data WHERE quantity IS NULL
UNION ALL
SELECT 'total_price' AS column_name, COUNT(*) AS null_count FROM data WHERE total_price IS NULL
UNION ALL
SELECT 'city' AS column_name, COUNT(*) AS null_count FROM data WHERE city IS NULL
ORDER BY null_count DESC;
```
---

## Duplicate order_id Values
**ARGS:** —
**Description:** Flags any order_id that appears more than once in the dataset.
```sql
SELECT order_id, COUNT(*) AS occurrences
FROM data
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
```
---

## Negative unit_price Values
**ARGS:** —
**Description:** Flags rows where unit_price is negative, which may indicate data errors.
```sql
SELECT *
FROM data
WHERE unit_price < 0
ORDER BY unit_price;
```
---

## Negative quantity Values
**ARGS:** —
**Description:** Flags rows where quantity is negative, which may indicate data errors.
```sql
SELECT *
FROM data
WHERE quantity < 0
ORDER BY quantity;
```
---

## Negative total_price Values
**ARGS:** —
**Description:** Flags rows where total_price is negative, which may indicate data errors.
```sql
SELECT *
FROM data
WHERE total_price < 0
ORDER BY total_price;
```
---
