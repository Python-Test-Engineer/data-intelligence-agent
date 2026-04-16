# SQL Test Results

Created: `2026-04-16 12:26:01`  
Original CSV: `uploaded.csv`  

Queries file: `C:\Users\mrcra\Desktop\data-intelligence-agent\output\sql\sql_queries_data.md`  
Source CSV: `C:\Users\mrcra\Desktop\data-intelligence-agent\data\data.csv` (in-memory SQLite)  
Queries run: **40** (all)

---

**Summary:** 26 passed · 0 failed · 14 skipped

---

## 1. Row Count

**Status:** OK

```sql
SELECT COUNT(*) AS row_count
FROM data;
```

**Rows returned:** 1

| row_count |
| --- |
| 3 |

---

## 2. Column Sample

**Status:** OK

```sql
SELECT *
FROM data
LIMIT 10;
```

**Rows returned:** 3

| order_id | product | category | city | quantity | unit_price | total_price |
| --- | --- | --- | --- | --- | --- | --- |
| ORD001 | Monitor | Electronics | New York | 10 | 349.99 | 3499.9 |
| ORD002 | Mouse | Accessories | London | 5 | 29.99 | 149.95 |
| ORD003 | Keyboard | Accessories | Paris | 8 | 79.99 | 639.92 |

---

## 3. Summary Stats for quantity

**Status:** OK

```sql
SELECT
    MIN(quantity) AS min_val,
    MAX(quantity) AS max_val,
    ROUND(AVG(quantity), 2) AS avg_val,
    SUM(quantity) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 5 | 10 | 7.67 | 23 |

---

## 4. Summary Stats for unit_price

**Status:** OK

```sql
SELECT
    MIN(unit_price) AS min_val,
    MAX(unit_price) AS max_val,
    ROUND(AVG(unit_price), 2) AS avg_val,
    SUM(unit_price) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 29.99 | 349.99 | 153.32 | 459.97 |

---

## 5. Summary Stats for total_price

**Status:** OK

```sql
SELECT
    MIN(total_price) AS min_val,
    MAX(total_price) AS max_val,
    ROUND(AVG(total_price), 2) AS avg_val,
    SUM(total_price) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 149.95 | 3499.9 | 1429.92 | 4289.77 |

---

## 6. Total quantity by product

**Status:** OK

```sql
SELECT product, SUM(quantity) AS total_quantity
FROM data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | total_quantity |
| --- | --- |
| Monitor | 10 |
| Keyboard | 8 |
| Mouse | 5 |

---

## 7. Average quantity by product

**Status:** OK

```sql
SELECT product, ROUND(AVG(quantity), 2) AS avg_quantity
FROM data
GROUP BY product
ORDER BY avg_quantity DESC;
```

**Rows returned:** 3

| product | avg_quantity |
| --- | --- |
| Monitor | 10.0 |
| Keyboard | 8.0 |
| Mouse | 5.0 |

---

## 8. Total unit_price by product

**Status:** OK

```sql
SELECT product, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY product
ORDER BY total_unit_price DESC;
```

**Rows returned:** 3

| product | total_unit_price |
| --- | --- |
| Monitor | 349.99 |
| Keyboard | 79.99 |
| Mouse | 29.99 |

---

## 9. Distribution of product

**Status:** OK

```sql
SELECT product, COUNT(*) AS row_count
FROM data
GROUP BY product
ORDER BY row_count DESC;
```

**Rows returned:** 3

| product | row_count |
| --- | --- |
| Mouse | 1 |
| Monitor | 1 |
| Keyboard | 1 |

---

## 10. Distribution of category

**Status:** OK

```sql
SELECT category, COUNT(*) AS row_count
FROM data
GROUP BY category
ORDER BY row_count DESC;
```

**Rows returned:** 2

| category | row_count |
| --- | --- |
| Accessories | 2 |
| Electronics | 1 |

---

## 11. Distribution of city

**Status:** OK

```sql
SELECT city, COUNT(*) AS row_count
FROM data
GROUP BY city
ORDER BY row_count DESC;
```

**Rows returned:** 3

| city | row_count |
| --- | --- |
| Paris | 1 |
| New York | 1 |
| London | 1 |

---

## 12. product Ranked by Total quantity

**Status:** OK

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | transaction_count | total_quantity |
| --- | --- | --- |
| Monitor | 1 | 10.0 |
| Keyboard | 1 | 8.0 |
| Mouse | 1 | 5.0 |

---

## 13. category Ranked by Total quantity

**Status:** OK

```sql
SELECT
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
GROUP BY category
ORDER BY total_quantity DESC;
```

**Rows returned:** 2

| category | transaction_count | total_quantity |
| --- | --- | --- |
| Accessories | 2 | 13.0 |
| Electronics | 1 | 10.0 |

---

## 14. city Ranked by Total quantity

**Status:** OK

```sql
SELECT
    city,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
GROUP BY city
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| city | transaction_count | total_quantity |
| --- | --- | --- |
| New York | 1 | 10.0 |
| Paris | 1 | 8.0 |
| London | 1 | 5.0 |

---

## 15. quantity by product and category

**Status:** OK

```sql
SELECT product, category, SUM(quantity) AS total_quantity
FROM data
GROUP BY product, category
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | category | total_quantity |
| --- | --- | --- |
| Monitor | Electronics | 10 |
| Keyboard | Accessories | 8 |
| Mouse | Accessories | 5 |

---

## 16. Performance Breakdown by product

**Status:** OK

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity,
    SUM(unit_price) AS total_unit_price,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY product
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | transaction_count | total_quantity | total_unit_price | total_total_price |
| --- | --- | --- | --- | --- |
| Monitor | 1 | 10 | 349.99 | 3499.9 |
| Keyboard | 1 | 8 | 79.99 | 639.92 |
| Mouse | 1 | 5 | 29.99 | 149.95 |

---

## 17. Performance Breakdown by category

**Status:** OK

```sql
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity,
    SUM(unit_price) AS total_unit_price,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY category
ORDER BY total_quantity DESC;
```

**Rows returned:** 2

| category | transaction_count | total_quantity | total_unit_price | total_total_price |
| --- | --- | --- | --- | --- |
| Accessories | 2 | 13 | 109.97999999999999 | 789.8699999999999 |
| Electronics | 1 | 10 | 349.99 | 3499.9 |

---

## 18. Performance Breakdown by city

**Status:** OK

```sql
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity,
    SUM(unit_price) AS total_unit_price,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY city
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| city | transaction_count | total_quantity | total_unit_price | total_total_price |
| --- | --- | --- | --- | --- |
| New York | 1 | 10 | 349.99 | 3499.9 |
| Paris | 1 | 8 | 79.99 | 639.92 |
| London | 1 | 5 | 29.99 | 149.95 |

---

## 19. product × category Performance Matrix

**Status:** OK

```sql
SELECT
    product,
    category,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity,
    SUM(unit_price) AS total_unit_price,
    SUM(total_price) AS total_total_price
FROM data
GROUP BY product, category
ORDER BY total_quantity DESC;
```

**Rows returned:** 3

| product | category | transaction_count | total_quantity | total_unit_price | total_total_price |
| --- | --- | --- | --- | --- | --- |
| Monitor | Electronics | 1 | 10 | 349.99 | 3499.9 |
| Keyboard | Accessories | 1 | 8 | 79.99 | 639.92 |
| Mouse | Accessories | 1 | 5 | 29.99 | 149.95 |

---

## 20. Unique order_id Count by product

**Status:** OK

```sql
SELECT
    product,
    COUNT(DISTINCT order_id) AS unique_order_id,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM data
GROUP BY product
ORDER BY unique_order_id DESC;
```

**Rows returned:** 3

| product | unique_order_id | transaction_count | total_quantity |
| --- | --- | --- | --- |
| Mouse | 1 | 1 | 5 |
| Monitor | 1 | 1 | 10 |
| Keyboard | 1 | 1 | 8 |

---

## 21. Unique order_id Count by category

**Status:** OK

```sql
SELECT
    category,
    COUNT(DISTINCT order_id) AS unique_order_id,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM data
GROUP BY category
ORDER BY unique_order_id DESC;
```

**Rows returned:** 2

| category | unique_order_id | transaction_count | total_quantity |
| --- | --- | --- | --- |
| Accessories | 2 | 2 | 13 |
| Electronics | 1 | 1 | 10 |

---

## 22. Filter by product

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE product = :product;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 23. Performance Summary for a Specific product

**Status:** SKIPPED

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM data
WHERE product = :product
GROUP BY product;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 24. category Breakdown for product = :product

**Status:** SKIPPED

```sql
SELECT
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
WHERE product = :product
GROUP BY category
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 25. city Breakdown for product = :product

**Status:** SKIPPED

```sql
SELECT
    city,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
WHERE product = :product
GROUP BY city
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 26. Filter by category

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE category = :category;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 27. Performance Summary for a Specific category

**Status:** SKIPPED

```sql
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM data
WHERE category = :category
GROUP BY category;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 28. product Breakdown for category = :category

**Status:** SKIPPED

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
WHERE category = :category
GROUP BY product
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 29. city Breakdown for category = :category

**Status:** SKIPPED

```sql
SELECT
    city,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
WHERE category = :category
GROUP BY city
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 30. Filter by city

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE city = :city;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 31. Performance Summary for a Specific city

**Status:** SKIPPED

```sql
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(quantity) AS total_quantity
FROM data
WHERE city = :city
GROUP BY city;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 32. product Breakdown for city = :city

**Status:** SKIPPED

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
WHERE city = :city
GROUP BY product
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 33. category Breakdown for city = :city

**Status:** SKIPPED

```sql
SELECT
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
WHERE city = :city
GROUP BY category
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 34. Rows Where quantity Exceeds :min_value

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE quantity > :min_value
ORDER BY quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 35. product with Total quantity Above :threshold

**Status:** SKIPPED

```sql
SELECT
    product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM data
GROUP BY product
HAVING SUM(quantity) > :threshold
ORDER BY total_quantity DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 36. Missing Values per Column

**Status:** OK

```sql
SELECT 'order_id' AS column_name, COUNT(*) AS null_count FROM data WHERE order_id IS NULL
UNION ALL
SELECT 'product' AS column_name, COUNT(*) AS null_count FROM data WHERE product IS NULL
UNION ALL
SELECT 'category' AS column_name, COUNT(*) AS null_count FROM data WHERE category IS NULL
UNION ALL
SELECT 'city' AS column_name, COUNT(*) AS null_count FROM data WHERE city IS NULL
UNION ALL
SELECT 'quantity' AS column_name, COUNT(*) AS null_count FROM data WHERE quantity IS NULL
UNION ALL
SELECT 'unit_price' AS column_name, COUNT(*) AS null_count FROM data WHERE unit_price IS NULL
UNION ALL
SELECT 'total_price' AS column_name, COUNT(*) AS null_count FROM data WHERE total_price IS NULL
ORDER BY null_count DESC;
```

**Rows returned:** 7

| column_name | null_count |
| --- | --- |
| order_id | 0 |
| product | 0 |
| category | 0 |
| city | 0 |
| quantity | 0 |
| unit_price | 0 |
| total_price | 0 |

---

## 37. Duplicate order_id Values

**Status:** OK

```sql
SELECT order_id, COUNT(*) AS occurrences
FROM data
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
```

**Rows returned:** 0

*(no rows returned)*

---

## 38. Negative quantity Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE quantity < 0
ORDER BY quantity;
```

**Rows returned:** 0

*(no rows returned)*

---

## 39. Negative unit_price Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE unit_price < 0
ORDER BY unit_price;
```

**Rows returned:** 0

*(no rows returned)*

---

## 40. Negative total_price Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE total_price < 0
ORDER BY total_price;
```

**Rows returned:** 0

*(no rows returned)*

---
