# SQL Query Catalog
<!-- source: data.csv | table: data | generated: 2026-03-27 | queries: 28 -->

---

### Overview

## Row Count
**ARGS:** —
**Description:** Returns the total number of rows in the dataset.
```sql
SELECT COUNT(*) AS row_count
FROM data;
```

**Status:** OK

**Rows returned:** 1

| row_count |
| --- |
| 20 |
---

## Column Sample
**ARGS:** —
**Description:** Returns the first 10 rows to preview the dataset structure.
```sql
SELECT *
FROM data
LIMIT 10;
```

**Status:** OK

**Rows returned:** 10

| order_id | date | product_name | unit_price | quantity | total_price | city |
| --- | --- | --- | --- | --- | --- | --- |
| ORD0001 | 2025-04-28 | Monitor | 349.99 | 10 | 3499.9 | New York |
| ORD0002 | 2025-09-29 | Mouse | 29.99 | 5 | 149.95 | New York |
| ORD0003 | 2025-08-04 | Headphones | 149.99 | 8 | 1199.92 | Chicago |
| ORD0004 | 2025-12-16 | Headphones | 149.99 | 6 | 899.94 | New York |
| ORD0005 | 2025-02-12 | Mouse | 29.99 | 3 | 89.97 | Los Angeles |
| ORD0008 | 2025-11-07 | Headphones | 149.99 | 9 | 1349.91 | Los Angeles |
| ORD0009 | 2025-03-24 | Monitor | 349.99 | 3 | 1049.97 | Los Angeles |
| ORD0011 | 2025-02-11 | Laptop | 999.99 | 8 | 7999.92 | New York |
| ORD0012 | 2025-07-15 | Monitor | 349.99 | 5 | 1749.95 | New York |
| ORD0013 | 2025-01-29 | Keyboard | 79.99 | 7 | 559.93 | Chicago |
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

**Status:** OK

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 29.99 | 999.99 | 403.49 | 8069.8 |
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

**Status:** OK

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 3 | 10 | 6.65 | 133 |
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

**Status:** OK

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 89.97 | 7999.92 | 2695.93 | 53918.67 |
---

## Total unit_price by date
**ARGS:** —
**Description:** Ranks each date by total unit_price, highest first.
```sql
SELECT date, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY date
ORDER BY total_unit_price DESC;
```

**Status:** OK

**Rows returned:** 18

| date | total_unit_price |
| --- | --- |
| 2025-04-28 | 1349.98 |
| 2025-09-25 | 999.99 |
| 2025-06-22 | 999.99 |
| 2025-03-26 | 999.99 |
| 2025-02-11 | 999.99 |
| 2025-04-10 | 499.98 |
| 2025-07-15 | 349.99 |
| 2025-03-24 | 349.99 |
| 2025-02-05 | 349.99 |
| 2025-01-02 | 349.99 |
| 2025-12-16 | 149.99 |
| 2025-11-07 | 149.99 |
| 2025-10-01 | 149.99 |
| 2025-08-04 | 149.99 |
| 2025-03-23 | 79.99 |
| 2025-01-29 | 79.99 |
| 2025-09-29 | 29.99 |
| 2025-02-12 | 29.99 |
---

## Average unit_price by date
**ARGS:** —
**Description:** Compares average unit_price across each date.
```sql
SELECT date, ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM data
GROUP BY date
ORDER BY avg_unit_price DESC;
```

**Status:** OK

**Rows returned:** 18

| date | avg_unit_price |
| --- | --- |
| 2025-09-25 | 999.99 |
| 2025-06-22 | 999.99 |
| 2025-03-26 | 999.99 |
| 2025-02-11 | 999.99 |
| 2025-04-28 | 674.99 |
| 2025-07-15 | 349.99 |
| 2025-03-24 | 349.99 |
| 2025-02-05 | 349.99 |
| 2025-01-02 | 349.99 |
| 2025-04-10 | 249.99 |
| 2025-12-16 | 149.99 |
| 2025-11-07 | 149.99 |
| 2025-10-01 | 149.99 |
| 2025-08-04 | 149.99 |
| 2025-03-23 | 79.99 |
| 2025-01-29 | 79.99 |
| 2025-09-29 | 29.99 |
| 2025-02-12 | 29.99 |
---

## Total quantity by date
**ARGS:** —
**Description:** Ranks each date by total quantity, highest first.
```sql
SELECT date, SUM(quantity) AS total_quantity
FROM data
GROUP BY date
ORDER BY total_quantity DESC;
```

**Status:** OK

**Rows returned:** 18

| date | total_quantity |
| --- | --- |
| 2025-04-28 | 17 |
| 2025-04-10 | 16 |
| 2025-11-07 | 9 |
| 2025-03-23 | 9 |
| 2025-08-04 | 8 |
| 2025-02-11 | 8 |
| 2025-06-22 | 7 |
| 2025-03-26 | 7 |
| 2025-02-05 | 7 |
| 2025-01-29 | 7 |
| 2025-12-16 | 6 |
| 2025-10-01 | 6 |
| 2025-01-02 | 6 |
| 2025-09-29 | 5 |
| 2025-07-15 | 5 |
| 2025-09-25 | 4 |
| 2025-03-24 | 3 |
| 2025-02-12 | 3 |
---

### Categorical Distributions

## Distribution of date
**ARGS:** —
**Description:** Counts rows for each distinct value of date, ordered by frequency.
```sql
SELECT date, COUNT(*) AS row_count
FROM data
GROUP BY date
ORDER BY row_count DESC;
```

**Status:** OK

**Rows returned:** 18

| date | row_count |
| --- | --- |
| 2025-04-28 | 2 |
| 2025-04-10 | 2 |
| 2025-12-16 | 1 |
| 2025-11-07 | 1 |
| 2025-10-01 | 1 |
| 2025-09-29 | 1 |
| 2025-09-25 | 1 |
| 2025-08-04 | 1 |
| 2025-07-15 | 1 |
| 2025-06-22 | 1 |
| 2025-03-26 | 1 |
| 2025-03-24 | 1 |
| 2025-03-23 | 1 |
| 2025-02-12 | 1 |
| 2025-02-11 | 1 |
| 2025-02-05 | 1 |
| 2025-01-29 | 1 |
| 2025-01-02 | 1 |
---

## Distribution of product_name
**ARGS:** —
**Description:** Counts rows for each distinct value of product_name, ordered by frequency.
```sql
SELECT product_name, COUNT(*) AS row_count
FROM data
GROUP BY product_name
ORDER BY row_count DESC;
```

**Status:** OK

**Rows returned:** 5

| product_name | row_count |
| --- | --- |
| Monitor | 6 |
| Laptop | 5 |
| Headphones | 5 |
| Mouse | 2 |
| Keyboard | 2 |
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

**Status:** OK

**Rows returned:** 3

| city | row_count |
| --- | --- |
| Los Angeles | 8 |
| New York | 7 |
| Chicago | 5 |
---

### Rankings

## Top 10 date by unit_price
**ARGS:** —
**Description:** Lists the 10 date values with the highest total unit_price.
```sql
SELECT date, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY date
ORDER BY total_unit_price DESC
LIMIT 10;
```

**Status:** OK

**Rows returned:** 10

| date | total_unit_price |
| --- | --- |
| 2025-04-28 | 1349.98 |
| 2025-09-25 | 999.99 |
| 2025-06-22 | 999.99 |
| 2025-03-26 | 999.99 |
| 2025-02-11 | 999.99 |
| 2025-04-10 | 499.98 |
| 2025-07-15 | 349.99 |
| 2025-03-24 | 349.99 |
| 2025-02-05 | 349.99 |
| 2025-01-02 | 349.99 |
---

## Bottom 10 date by unit_price
**ARGS:** —
**Description:** Lists the 10 date values with the lowest total unit_price.
```sql
SELECT date, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY date
ORDER BY total_unit_price ASC
LIMIT 10;
```

**Status:** OK

**Rows returned:** 10

| date | total_unit_price |
| --- | --- |
| 2025-02-12 | 29.99 |
| 2025-09-29 | 29.99 |
| 2025-01-29 | 79.99 |
| 2025-03-23 | 79.99 |
| 2025-08-04 | 149.99 |
| 2025-10-01 | 149.99 |
| 2025-11-07 | 149.99 |
| 2025-12-16 | 149.99 |
| 2025-01-02 | 349.99 |
| 2025-02-05 | 349.99 |
---

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

**Status:** OK

**Rows returned:** 5

| product_name | total_unit_price |
| --- | --- |
| Laptop | 4999.95 |
| Monitor | 2099.94 |
| Headphones | 749.95 |
| Keyboard | 159.98 |
| Mouse | 59.98 |
---

### Multi-Dimensional

## unit_price by date and product_name
**ARGS:** —
**Description:** Shows total unit_price broken down by both date and product_name.
```sql
SELECT date, product_name, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY date, product_name
ORDER BY total_unit_price DESC;
```

**Status:** OK

**Rows returned:** 20

| date | product_name | total_unit_price |
| --- | --- | --- |
| 2025-02-11 | Laptop | 999.99 |
| 2025-03-26 | Laptop | 999.99 |
| 2025-04-28 | Laptop | 999.99 |
| 2025-06-22 | Laptop | 999.99 |
| 2025-09-25 | Laptop | 999.99 |
| 2025-01-02 | Monitor | 349.99 |
| 2025-02-05 | Monitor | 349.99 |
| 2025-03-24 | Monitor | 349.99 |
| 2025-04-10 | Monitor | 349.99 |
| 2025-04-28 | Monitor | 349.99 |
| 2025-07-15 | Monitor | 349.99 |
| 2025-04-10 | Headphones | 149.99 |
| 2025-08-04 | Headphones | 149.99 |
| 2025-10-01 | Headphones | 149.99 |
| 2025-11-07 | Headphones | 149.99 |
| 2025-12-16 | Headphones | 149.99 |
| 2025-01-29 | Keyboard | 79.99 |
| 2025-03-23 | Keyboard | 79.99 |
| 2025-02-12 | Mouse | 29.99 |
| 2025-09-29 | Mouse | 29.99 |
---

### Multi-Metric Analysis

## Performance Breakdown by date
**ARGS:** —
**Description:** Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by date.
```sql
SELECT
    date,
    COUNT(*) AS transaction_count,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY date
ORDER BY total_unit_price DESC;
```

**Status:** OK

**Rows returned:** 18

| date | transaction_count | total_unit_price | total_quantity | total_total_price |
| --- | --- | --- | --- | --- |
| 2025-04-28 | 2 | 1349.98 | 17 | 10499.83 |
| 2025-09-25 | 1 | 999.99 | 4 | 3999.96 |
| 2025-06-22 | 1 | 999.99 | 7 | 6999.93 |
| 2025-03-26 | 1 | 999.99 | 7 | 6999.93 |
| 2025-02-11 | 1 | 999.99 | 8 | 7999.92 |
| 2025-04-10 | 2 | 499.98 | 16 | 4199.84 |
| 2025-07-15 | 1 | 349.99 | 5 | 1749.95 |
| 2025-03-24 | 1 | 349.99 | 3 | 1049.97 |
| 2025-02-05 | 1 | 349.99 | 7 | 2449.93 |
| 2025-01-02 | 1 | 349.99 | 6 | 2099.94 |
| 2025-12-16 | 1 | 149.99 | 6 | 899.94 |
| 2025-11-07 | 1 | 149.99 | 9 | 1349.91 |
| 2025-10-01 | 1 | 149.99 | 6 | 899.94 |
| 2025-08-04 | 1 | 149.99 | 8 | 1199.92 |
| 2025-03-23 | 1 | 79.99 | 9 | 719.91 |
| 2025-01-29 | 1 | 79.99 | 7 | 559.93 |
| 2025-09-29 | 1 | 29.99 | 5 | 149.95 |
| 2025-02-12 | 1 | 29.99 | 3 | 89.97 |
---

## Performance Breakdown by product_name
**ARGS:** —
**Description:** Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by product_name.
```sql
SELECT
    product_name,
    COUNT(*) AS transaction_count,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY product_name
ORDER BY total_unit_price DESC;
```

**Status:** OK

**Rows returned:** 5

| product_name | transaction_count | total_unit_price | total_quantity | total_total_price |
| --- | --- | --- | --- | --- |
| Laptop | 5 | 4999.95 | 33 | 32999.67 |
| Monitor | 6 | 2099.94 | 40 | 13999.6 |
| Headphones | 5 | 749.95 | 36 | 5399.64 |
| Keyboard | 2 | 159.98 | 16 | 1279.84 |
| Mouse | 2 | 59.98 | 8 | 239.92 |
---

## Performance Breakdown by city
**ARGS:** —
**Description:** Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by city.
```sql
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY city
ORDER BY total_unit_price DESC;
```

**Status:** OK

**Rows returned:** 3

| city | transaction_count | total_unit_price | total_quantity | total_total_price |
| --- | --- | --- | --- | --- |
| New York | 7 | 2959.93 | 50 | 22019.5 |
| Los Angeles | 8 | 2729.92 | 51 | 18239.49 |
| Chicago | 5 | 2379.95 | 32 | 13659.68 |
---

## date × product_name Performance Matrix
**ARGS:** —
**Description:** Shows performance metrics for every date and product_name combination, ordered by profitability.
```sql
SELECT
    date,
    product_name,
    COUNT(*) AS transaction_count,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY date, product_name
ORDER BY total_unit_price DESC;
```

**Status:** OK

**Rows returned:** 20

| date | product_name | transaction_count | total_unit_price | total_quantity | total_total_price |
| --- | --- | --- | --- | --- | --- |
| 2025-02-11 | Laptop | 1 | 999.99 | 8 | 7999.92 |
| 2025-03-26 | Laptop | 1 | 999.99 | 7 | 6999.93 |
| 2025-04-28 | Laptop | 1 | 999.99 | 7 | 6999.93 |
| 2025-06-22 | Laptop | 1 | 999.99 | 7 | 6999.93 |
| 2025-09-25 | Laptop | 1 | 999.99 | 4 | 3999.96 |
| 2025-01-02 | Monitor | 1 | 349.99 | 6 | 2099.94 |
| 2025-02-05 | Monitor | 1 | 349.99 | 7 | 2449.93 |
| 2025-03-24 | Monitor | 1 | 349.99 | 3 | 1049.97 |
| 2025-04-10 | Monitor | 1 | 349.99 | 9 | 3149.91 |
| 2025-04-28 | Monitor | 1 | 349.99 | 10 | 3499.9 |
| 2025-07-15 | Monitor | 1 | 349.99 | 5 | 1749.95 |
| 2025-04-10 | Headphones | 1 | 149.99 | 7 | 1049.93 |
| 2025-08-04 | Headphones | 1 | 149.99 | 8 | 1199.92 |
| 2025-10-01 | Headphones | 1 | 149.99 | 6 | 899.94 |
| 2025-11-07 | Headphones | 1 | 149.99 | 9 | 1349.91 |
| 2025-12-16 | Headphones | 1 | 149.99 | 6 | 899.94 |
| 2025-01-29 | Keyboard | 1 | 79.99 | 7 | 559.93 |
| 2025-03-23 | Keyboard | 1 | 79.99 | 9 | 719.91 |
| 2025-02-12 | Mouse | 1 | 29.99 | 3 | 89.97 |
| 2025-09-29 | Mouse | 1 | 29.99 | 5 | 149.95 |
---

## Unique order_id Count by date
**ARGS:** —
**Description:** Counts distinct order_id values and key metrics per date to reveal concentration.
```sql
SELECT
    date,
    COUNT(DISTINCT order_id) AS unique_order_id,
    COUNT(*) AS transaction_count,
    SUM(unit_price) AS total_unit_price
FROM data
GROUP BY date
ORDER BY unique_order_id DESC;
```

**Status:** OK

**Rows returned:** 18

| date | unique_order_id | transaction_count | total_unit_price |
| --- | --- | --- | --- |
| 2025-04-28 | 2 | 2 | 1349.98 |
| 2025-04-10 | 2 | 2 | 499.98 |
| 2025-12-16 | 1 | 1 | 149.99 |
| 2025-11-07 | 1 | 1 | 149.99 |
| 2025-10-01 | 1 | 1 | 149.99 |
| 2025-09-29 | 1 | 1 | 29.99 |
| 2025-09-25 | 1 | 1 | 999.99 |
| 2025-08-04 | 1 | 1 | 149.99 |
| 2025-07-15 | 1 | 1 | 349.99 |
| 2025-06-22 | 1 | 1 | 999.99 |
| 2025-03-26 | 1 | 1 | 999.99 |
| 2025-03-24 | 1 | 1 | 349.99 |
| 2025-03-23 | 1 | 1 | 79.99 |
| 2025-02-12 | 1 | 1 | 29.99 |
| 2025-02-11 | 1 | 1 | 999.99 |
| 2025-02-05 | 1 | 1 | 349.99 |
| 2025-01-29 | 1 | 1 | 79.99 |
| 2025-01-02 | 1 | 1 | 349.99 |
---

## Unique order_id Count by product_name
**ARGS:** —
**Description:** Counts distinct order_id values and key metrics per product_name to reveal concentration.
```sql
SELECT
    product_name,
    COUNT(DISTINCT order_id) AS unique_order_id,
    COUNT(*) AS transaction_count,
    SUM(unit_price) AS total_unit_price
FROM data
GROUP BY product_name
ORDER BY unique_order_id DESC;
```

**Status:** OK

**Rows returned:** 5

| product_name | unique_order_id | transaction_count | total_unit_price |
| --- | --- | --- | --- |
| Monitor | 6 | 6 | 2099.94 |
| Laptop | 5 | 5 | 4999.95 |
| Headphones | 5 | 5 | 749.95 |
| Mouse | 2 | 2 | 59.98 |
| Keyboard | 2 | 2 | 159.98 |
---

### Parametric Lookups

## Filter by date
**ARGS:** date
**Description:** Returns all rows where date matches a given value.
```sql
SELECT *
FROM data
WHERE date = :date;
```

**Status:** SKIPPED

**Skipped:** Query requires runtime arguments (:param)
---

## Total unit_price for a Specific date
**ARGS:** date
**Description:** Returns total unit_price for a single date value.
```sql
SELECT date, SUM(unit_price) AS total_unit_price
FROM data
WHERE date = :date
GROUP BY date;
```

**Status:** SKIPPED

**Skipped:** Query requires runtime arguments (:param)
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

**Status:** OK

**Rows returned:** 7

| column_name | null_count |
| --- | --- |
| order_id | 0 |
| date | 0 |
| product_name | 0 |
| unit_price | 0 |
| quantity | 0 |
| total_price | 0 |
| city | 0 |
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

**Status:** OK

**Rows returned:** 0

*(no rows returned)*
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

**Status:** OK

**Rows returned:** 0

*(no rows returned)*
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

**Status:** OK

**Rows returned:** 0

*(no rows returned)*
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

**Status:** OK

**Rows returned:** 0

*(no rows returned)*
---