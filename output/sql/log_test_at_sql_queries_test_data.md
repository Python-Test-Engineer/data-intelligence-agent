# SQL Test Results

Created: `2026-04-16 12:28:25`  
Original CSV: `uploaded.csv`  

Queries file: `C:\Users\mrcra\Desktop\data-intelligence-agent\output\sql\sql_queries_test_data.md`  
Source CSV: `C:\Users\mrcra\AppData\Local\Temp\pytest-of-mrcra\pytest-30\test_run_tests_and_merge_inlin0\test_data.csv` (in-memory SQLite)  
Queries run: **17** (all)

---

**Summary:** 13 passed · 0 failed · 4 skipped

---

## 1. Row Count

**Status:** OK

```sql
SELECT COUNT(*) AS row_count
FROM test_data;
```

**Rows returned:** 1

| row_count |
| --- |
| 4 |

---

## 2. Column Sample

**Status:** OK

```sql
SELECT *
FROM test_data
LIMIT 10;
```

**Rows returned:** 4

| product | quantity | price |
| --- | --- | --- |
| A | 10 | 1.0 |
| B | 20 | 2.0 |
| A | 15 | 1.5 |
| C | 5 | 3.0 |

---

## 3. Summary Stats for quantity

**Status:** OK

```sql
SELECT
    MIN(quantity) AS min_val,
    MAX(quantity) AS max_val,
    ROUND(AVG(quantity), 2) AS avg_val,
    SUM(quantity) AS total
FROM test_data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 5 | 20 | 12.5 | 50 |

---

## 4. Summary Stats for price

**Status:** OK

```sql
SELECT
    MIN(price) AS min_val,
    MAX(price) AS max_val,
    ROUND(AVG(price), 2) AS avg_val,
    SUM(price) AS total
FROM test_data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 1.0 | 3.0 | 1.88 | 7.5 |

---

## 5. Total quantity by product

**Status:** OK

```sql
SELECT product, SUM(quantity) AS total_quantity
FROM test_data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | total_quantity |
| --- | --- |
| A | 25 |
| B | 20 |
| C | 5 |

---

## 6. Average quantity by product

**Status:** OK

```sql
SELECT product, ROUND(AVG(quantity), 2) AS avg_quantity
FROM test_data
GROUP BY product
ORDER BY avg_quantity DESC;
```

**Rows returned:** 3

| product | avg_quantity |
| --- | --- |
| B | 20.0 |
| A | 12.5 |
| C | 5.0 |

---

## 7. Total price by product

**Status:** OK

```sql
SELECT product, SUM(price) AS total_price
FROM test_data
GROUP BY product
ORDER BY total_price DESC;
```

**Rows returned:** 3

| product | total_price |
| --- | --- |
| C | 3.0 |
| A | 2.5 |
| B | 2.0 |

---

## 8. Distribution of product

**Status:** OK

```sql
SELECT product, COUNT(*) AS row_count
FROM test_data
GROUP BY product
ORDER BY row_count DESC;
```

**Rows returned:** 3

| product | row_count |
| --- | --- |
| A | 2 |
| C | 1 |
| B | 1 |

---

## 9. product Ranked by Total quantity

**Status:** OK

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM test_data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | transaction_count | total_quantity |
| --- | --- | --- |
| A | 2 | 25.0 |
| B | 1 | 20.0 |
| C | 1 | 5.0 |

---

## 10. Performance Breakdown by product

**Status:** OK

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

**Rows returned:** 3

| product | transaction_count | total_quantity | total_price |
| --- | --- | --- | --- |
| A | 2 | 25 | 2.5 |
| B | 1 | 20 | 2.0 |
| C | 1 | 5 | 3.0 |

---

## 11. Filter by product

**Status:** SKIPPED

```sql
SELECT *
FROM test_data
WHERE product = :product;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 12. Performance Summary for a Specific product

**Status:** SKIPPED

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM test_data
WHERE product = :product
GROUP BY product;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 13. Rows Where quantity Exceeds :min_value

**Status:** SKIPPED

```sql
SELECT *
FROM test_data
WHERE quantity > :min_value
ORDER BY quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 14. product with Total quantity Above :threshold

**Status:** SKIPPED

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

**Skipped:** Query requires runtime arguments (:param)

---

## 15. Missing Values per Column

**Status:** OK

```sql
SELECT 'product' AS column_name, COUNT(*) AS null_count FROM test_data WHERE product IS NULL
UNION ALL
SELECT 'quantity' AS column_name, COUNT(*) AS null_count FROM test_data WHERE quantity IS NULL
UNION ALL
SELECT 'price' AS column_name, COUNT(*) AS null_count FROM test_data WHERE price IS NULL
ORDER BY null_count DESC;
```

**Rows returned:** 3

| column_name | null_count |
| --- | --- |
| product | 0 |
| quantity | 0 |
| price | 0 |

---

## 16. Negative quantity Values

**Status:** OK

```sql
SELECT *
FROM test_data
WHERE quantity < 0
ORDER BY quantity;
```

**Rows returned:** 0

*(no rows returned)*

---

## 17. Negative price Values

**Status:** OK

```sql
SELECT *
FROM test_data
WHERE price < 0
ORDER BY price;
```

**Rows returned:** 0

*(no rows returned)*

---
