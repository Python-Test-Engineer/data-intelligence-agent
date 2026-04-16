# SQL Query Catalog
<!-- source: test_data.csv | table: test_data | generated: 2026-04-16 | queries: 17 -->

---

### Overview

## Row Count
**ARGS:** —
**Description:** Returns the total number of rows in the dataset.
```sql
SELECT COUNT(*) AS row_count
FROM test_data;
```

**Status:** OK

**Rows returned:** 1

| row_count |
| --- |
| 4 |
---

## Column Sample
**ARGS:** —
**Description:** Returns the first 10 rows to preview the dataset structure.
```sql
SELECT *
FROM test_data
LIMIT 10;
```

**Status:** OK

**Rows returned:** 4

| product | quantity | price |
| --- | --- | --- |
| A | 10 | 1.0 |
| B | 20 | 2.0 |
| A | 15 | 1.5 |
| C | 5 | 3.0 |
---

### Numeric Summaries

## Summary Stats for quantity
**ARGS:** —
**Description:** Returns min, max, average, and total for quantity.
```sql
SELECT
    MIN(quantity) AS min_val,
    MAX(quantity) AS max_val,
    ROUND(AVG(quantity), 2) AS avg_val,
    SUM(quantity) AS total
FROM test_data;
```

**Status:** OK

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 5 | 20 | 12.5 | 50 |
---

## Summary Stats for price
**ARGS:** —
**Description:** Returns min, max, average, and total for price.
```sql
SELECT
    MIN(price) AS min_val,
    MAX(price) AS max_val,
    ROUND(AVG(price), 2) AS avg_val,
    SUM(price) AS total
FROM test_data;
```

**Status:** OK

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 1.0 | 3.0 | 1.88 | 7.5 |
---

## Total quantity by product
**ARGS:** —
**Description:** Ranks each product by total quantity, highest first.
```sql
SELECT product, SUM(quantity) AS total_quantity
FROM test_data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Status:** OK

**Rows returned:** 3

| product | total_quantity |
| --- | --- |
| A | 25 |
| B | 20 |
| C | 5 |
---

## Average quantity by product
**ARGS:** —
**Description:** Compares average quantity across each product.
```sql
SELECT product, ROUND(AVG(quantity), 2) AS avg_quantity
FROM test_data
GROUP BY product
ORDER BY avg_quantity DESC;
```

**Status:** OK

**Rows returned:** 3

| product | avg_quantity |
| --- | --- |
| B | 20.0 |
| A | 12.5 |
| C | 5.0 |
---

## Total price by product
**ARGS:** —
**Description:** Ranks each product by total price, highest first.
```sql
SELECT product, SUM(price) AS total_price
FROM test_data
GROUP BY product
ORDER BY total_price DESC;
```

**Status:** OK

**Rows returned:** 3

| product | total_price |
| --- | --- |
| C | 3.0 |
| A | 2.5 |
| B | 2.0 |
---

### Categorical Distributions

## Distribution of product
**ARGS:** —
**Description:** Counts rows for each distinct value of product, ordered by frequency.
```sql
SELECT product, COUNT(*) AS row_count
FROM test_data
GROUP BY product
ORDER BY row_count DESC;
```

**Status:** OK

**Rows returned:** 3

| product | row_count |
| --- | --- |
| A | 2 |
| C | 1 |
| B | 1 |
---

### Rankings

## product Ranked by Total quantity
**ARGS:** —
**Description:** Ranks each product by total quantity, highest first.
```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM test_data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Status:** OK

**Rows returned:** 3

| product | transaction_count | total_quantity |
| --- | --- | --- |
| A | 2 | 25.0 |
| B | 1 | 20.0 |
| C | 1 | 5.0 |
---

### Multi-Metric Analysis

## Performance Breakdown by product
**ARGS:** —
**Description:** Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by product.
```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity,
    SUM(price) AS total_price
FROM test_data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Status:** OK

**Rows returned:** 3

| product | transaction_count | total_quantity | total_price |
| --- | --- | --- | --- |
| A | 2 | 25 | 2.5 |
| B | 1 | 20 | 2.0 |
| C | 1 | 5 | 3.0 |
---

### Parametric Lookups

## Filter by product
**ARGS:** product
**Description:** Returns all rows where product matches a given value.
```sql
SELECT *
FROM test_data
WHERE product = :product;
```

**Status:** SKIPPED

**Skipped:** Query requires runtime arguments (:param)
---

## Performance Summary for a Specific product
**ARGS:** product
**Description:** Returns transaction count and all key metrics for a single product value.
```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM test_data
WHERE product = :product
GROUP BY product;
```

**Status:** SKIPPED

**Skipped:** Query requires runtime arguments (:param)
---

## Rows Where quantity Exceeds :min_value
**ARGS:** min_value
**Description:** Returns all rows where quantity is above a given threshold.
```sql
SELECT *
FROM test_data
WHERE quantity > :min_value
ORDER BY quantity DESC;
```

**Status:** SKIPPED

**Skipped:** Query requires runtime arguments (:param)
---

## product with Total quantity Above :threshold
**ARGS:** threshold
**Description:** Lists product values whose total quantity exceeds a given threshold.
```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM test_data
GROUP BY product
HAVING SUM(quantity) > :threshold
ORDER BY total_quantity DESC;
```

**Status:** SKIPPED

**Skipped:** Query requires runtime arguments (:param)
---

### Data Quality Checks

## Missing Values per Column
**ARGS:** —
**Description:** Counts NULL values in each column to identify data gaps.
```sql
SELECT 'product' AS column_name, COUNT(*) AS null_count FROM test_data WHERE product IS NULL
UNION ALL
SELECT 'quantity' AS column_name, COUNT(*) AS null_count FROM test_data WHERE quantity IS NULL
UNION ALL
SELECT 'price' AS column_name, COUNT(*) AS null_count FROM test_data WHERE price IS NULL
ORDER BY null_count DESC;
```

**Status:** OK

**Rows returned:** 3

| column_name | null_count |
| --- | --- |
| product | 0 |
| quantity | 0 |
| price | 0 |
---

## Negative quantity Values
**ARGS:** —
**Description:** Flags rows where quantity is negative, which may indicate data errors.
```sql
SELECT *
FROM test_data
WHERE quantity < 0
ORDER BY quantity;
```

**Status:** OK

**Rows returned:** 0

*(no rows returned)*
---

## Negative price Values
**ARGS:** —
**Description:** Flags rows where price is negative, which may indicate data errors.
```sql
SELECT *
FROM test_data
WHERE price < 0
ORDER BY price;
```

**Status:** OK

**Rows returned:** 0

*(no rows returned)*
---