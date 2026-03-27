# SQL Test Results

Created: `2026-03-27 16:47:07`  
Original CSV: `sales_data_100.csv`  

Queries file: `C:\Users\mrcra\Desktop\data-intelligence-agent\output\sql\sql_queries_data.md`  
Source CSV: `data\data.csv` (in-memory SQLite)  
Queries run: **33** (all)

---

**Summary:** 30 passed · 1 failed · 2 skipped

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
| 100 |

---

## 2. Column Sample

**Status:** OK

```sql
SELECT *
FROM data
LIMIT 10;
```

**Rows returned:** 10

| order_id | date | customer_id | customer_name | product_id | product_name | unit_cost | unit_price | quantity | total_cost | total_revenue | profit | margin_pct | store_id | store_name | city | payment_method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORD0001 | 2025-02-28 | C06 | Frank Miller | P003 | Keyboard | 28.0 | 79.99 | 4 | 112.0 | 319.96 | 207.96 | 65.0 | S1 | Store Alpha | New York | Debit Card |
| ORD0002 | 2025-03-16 | C08 | Henry Moore | P003 | Keyboard | 28.0 | 79.99 | 10 | 280.0 | 799.9 | 519.9 | 65.0 | S3 | Store Gamma | Chicago | Debit Card |
| ORD0003 | 2025-09-12 | C09 | Isabella Taylor | P005 | Headphones | 55.0 | 149.99 | 5 | 275.0 | 749.95 | 474.95 | 63.3 | S1 | Store Alpha | New York | Credit Card |
| ORD0004 | 2025-06-19 | C04 | David Brown | P002 | Mouse | 8.5 | 29.99 | 7 | 59.5 | 209.93 | 150.43 | 71.7 | S3 | Store Gamma | Chicago | Debit Card |
| ORD0005 | 2025-10-01 | C02 | Bob Smith | P003 | Keyboard | 28.0 | 79.99 | 9 | 252.0 | 719.91 | 467.91 | 65.0 | S1 | Store Alpha | New York | Cash |
| ORD0006 | 2025-02-11 | C04 | David Brown | P004 | Monitor | 180.0 | 349.99 | 4 | 720.0 | 1399.96 | 679.96 | 48.6 | S1 | Store Alpha | New York | Credit Card |
| ORD0007 | 2025-02-21 | C09 | Isabella Taylor | P002 | Mouse | 8.5 | 29.99 | 10 | 85.0 | 299.9 | 214.9 | 71.7 | S2 | Store Beta | Los Angeles | Credit Card |
| ORD0008 | 2025-02-10 | C06 | Frank Miller | P002 | Mouse | 8.5 | 29.99 | 2 | 17.0 | 59.98 | 42.98 | 71.7 | S1 | Store Alpha | New York | PayPal |
| ORD0009 | 2025-06-29 | C02 | Bob Smith | P005 | Headphones | 55.0 | 149.99 | 8 | 440.0 | 1199.92 | 759.92 | 63.3 | S2 | Store Beta | Los Angeles | Credit Card |
| ORD0039 | 2025-06-16 | C04 | David Brown | P004 | Monitor | 180.0 | 349.99 | 10 | 1800.0 | 3499.9 | 1699.9 | 48.6 | S3 | Store Gamma | Chicago | Cash |

---

## 3. Summary Stats for unit_cost

**Status:** OK

```sql
SELECT
    MIN(unit_cost) AS min_val,
    MAX(unit_cost) AS max_val,
    ROUND(AVG(unit_cost), 2) AS avg_val,
    SUM(unit_cost) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 8.5 | 650.0 | 219.84 | 21764.5 |

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
| 29.99 | 999.99 | 376.69 | 37669.0 |

---

## 5. Summary Stats for quantity

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
| -1 | 10 | 6.12 | 612 |

---

## 6. Summary Stats for total_cost

**Status:** OK

```sql
SELECT
    MIN(total_cost) AS min_val,
    MAX(total_cost) AS max_val,
    ROUND(AVG(total_cost), 2) AS avg_val,
    SUM(total_cost) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 17.0 | 6500.0 | 1341.73 | 131490.0 |

---

## 7. Summary Stats for total_revenue

**Status:** OK

```sql
SELECT
    MIN(total_revenue) AS min_val,
    MAX(total_revenue) AS max_val,
    ROUND(AVG(total_revenue), 2) AS avg_val,
    SUM(total_revenue) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 59.98 | 9999.9 | 2308.02 | 228493.87 |

---

## 8. Summary Stats for profit

**Status:** OK

```sql
SELECT
    MIN(profit) AS min_val,
    MAX(profit) AS max_val,
    ROUND(AVG(profit), 2) AS avg_val,
    SUM(profit) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 42.98 | 3499.9 | 964.84 | 94553.94 |

---

## 9. Total unit_cost by customer_name

**Status:** OK

```sql
SELECT customer_name, SUM(unit_cost) AS total_unit_cost
FROM data
GROUP BY customer_name
ORDER BY total_unit_cost DESC;
```

**Rows returned:** 11

| customer_name | total_unit_cost |
| --- | --- |
| Bob Smith | 4200.5 |
| Alice Johnson | 3378.0 |
| Isabella Taylor | 3259.5 |
| David Brown | 2840.0 |
| Grace Wilson | 1917.5 |
| Emma Davis | 1735.0 |
| Frank Miller | 1533.5 |
| Henry Moore | 1024.0 |
| Jack Anderson | 913.0 |
| Carol White | 783.5 |
| None | 180.0 |

---

## 10. Average unit_cost by customer_name

**Status:** OK

```sql
SELECT customer_name, ROUND(AVG(unit_cost), 2) AS avg_unit_cost
FROM data
GROUP BY customer_name
ORDER BY avg_unit_cost DESC;
```

**Rows returned:** 11

| customer_name | avg_unit_cost |
| --- | --- |
| Alice Johnson | 337.8 |
| Isabella Taylor | 296.32 |
| Bob Smith | 262.53 |
| Jack Anderson | 228.25 |
| Frank Miller | 219.07 |
| David Brown | 202.86 |
| None | 180.0 |
| Grace Wilson | 174.32 |
| Henry Moore | 146.29 |
| Emma Davis | 144.58 |
| Carol White | 130.58 |

---

## 11. Total unit_price by customer_name

**Status:** OK

```sql
SELECT customer_name, SUM(unit_price) AS total_unit_price
FROM data
GROUP BY customer_name
ORDER BY total_unit_price DESC;
```

**Rows returned:** 11

| customer_name | total_unit_price |
| --- | --- |
| Bob Smith | 7049.84 |
| Isabella Taylor | 5739.88 |
| Alice Johnson | 5369.9 |
| David Brown | 5089.86 |
| Grace Wilson | 3419.89 |
| Emma Davis | 3079.88 |
| Frank Miller | 2519.93 |
| Henry Moore | 1889.93 |
| Jack Anderson | 1579.96 |
| Carol White | 1579.94 |
| None | 349.99 |

---

## 12. Distribution of customer_name

**Status:** OK

```sql
SELECT customer_name, COUNT(*) AS row_count
FROM data
GROUP BY customer_name
ORDER BY row_count DESC;
```

**Rows returned:** 11

| customer_name | row_count |
| --- | --- |
| Bob Smith | 16 |
| David Brown | 14 |
| Isabella Taylor | 12 |
| Emma Davis | 12 |
| Grace Wilson | 11 |
| Alice Johnson | 10 |
| Henry Moore | 7 |
| Frank Miller | 7 |
| Carol White | 6 |
| Jack Anderson | 4 |
| None | 1 |

---

## 13. Distribution of product_name

**Status:** OK

```sql
SELECT product_name, COUNT(*) AS row_count
FROM data
GROUP BY product_name
ORDER BY row_count DESC;
```

**Rows returned:** 6

| product_name | row_count |
| --- | --- |
| Monitor | 27 |
| Laptop | 24 |
| Keyboard | 19 |
| Headphones | 15 |
| Mouse | 14 |
| Mousse | 1 |

---

## 14. Distribution of store_name

**Status:** OK

```sql
SELECT store_name, COUNT(*) AS row_count
FROM data
GROUP BY store_name
ORDER BY row_count DESC;
```

**Rows returned:** 3

| store_name | row_count |
| --- | --- |
| Store Gamma | 37 |
| Store Beta | 34 |
| Store Alpha | 29 |

---

## 15. Distribution of city

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
| Chicago | 37 |
| Los Angeles | 34 |
| New York | 29 |

---

## 16. Distribution of payment_method

**Status:** OK

```sql
SELECT payment_method, COUNT(*) AS row_count
FROM data
GROUP BY payment_method
ORDER BY row_count DESC;
```

**Rows returned:** 4

| payment_method | row_count |
| --- | --- |
| Credit Card | 31 |
| Cash | 26 |
| Debit Card | 23 |
| PayPal | 20 |

---

## 17. Top 10 customer_name by unit_cost

**Status:** OK

```sql
SELECT customer_name, SUM(unit_cost) AS total_unit_cost
FROM data
GROUP BY customer_name
ORDER BY total_unit_cost DESC
LIMIT 10;
```

**Rows returned:** 10

| customer_name | total_unit_cost |
| --- | --- |
| Bob Smith | 4200.5 |
| Alice Johnson | 3378.0 |
| Isabella Taylor | 3259.5 |
| David Brown | 2840.0 |
| Grace Wilson | 1917.5 |
| Emma Davis | 1735.0 |
| Frank Miller | 1533.5 |
| Henry Moore | 1024.0 |
| Jack Anderson | 913.0 |
| Carol White | 783.5 |

---

## 18. Bottom 10 customer_name by unit_cost

**Status:** OK

```sql
SELECT customer_name, SUM(unit_cost) AS total_unit_cost
FROM data
GROUP BY customer_name
ORDER BY total_unit_cost ASC
LIMIT 10;
```

**Rows returned:** 10

| customer_name | total_unit_cost |
| --- | --- |
| None | 180.0 |
| Carol White | 783.5 |
| Jack Anderson | 913.0 |
| Henry Moore | 1024.0 |
| Frank Miller | 1533.5 |
| Emma Davis | 1735.0 |
| Grace Wilson | 1917.5 |
| David Brown | 2840.0 |
| Isabella Taylor | 3259.5 |
| Alice Johnson | 3378.0 |

---

## 19. Top 10 product_name by unit_cost

**Status:** OK

```sql
SELECT product_name, SUM(unit_cost) AS total_unit_cost
FROM data
GROUP BY product_name
ORDER BY total_unit_cost DESC
LIMIT 10;
```

**Rows returned:** 6

| product_name | total_unit_cost |
| --- | --- |
| Laptop | 15600.0 |
| Monitor | 4680.0 |
| Headphones | 825.0 |
| Keyboard | 532.0 |
| Mouse | 119.0 |
| Mousse | 8.5 |

---

## 20. unit_cost by customer_name and product_name

**Status:** OK

```sql
SELECT customer_name, product_name, SUM(unit_cost) AS total_unit_cost
FROM data
GROUP BY customer_name, product_name
ORDER BY total_unit_cost DESC;
```

**Rows returned:** 46

| customer_name | product_name | total_unit_cost |
| --- | --- | --- |
| Alice Johnson | Laptop | 3250.0 |
| Bob Smith | Laptop | 3250.0 |
| Isabella Taylor | Laptop | 2600.0 |
| David Brown | Monitor | 1440.0 |
| David Brown | Laptop | 1300.0 |
| Emma Davis | Laptop | 1300.0 |
| Frank Miller | Laptop | 1300.0 |
| Grace Wilson | Laptop | 1300.0 |
| Bob Smith | Monitor | 720.0 |
| Carol White | Monitor | 720.0 |
| Henry Moore | Laptop | 650.0 |
| Jack Anderson | Laptop | 650.0 |
| Isabella Taylor | Monitor | 540.0 |
| Grace Wilson | Monitor | 360.0 |
| None | Monitor | 180.0 |
| Emma Davis | Monitor | 180.0 |
| Frank Miller | Monitor | 180.0 |
| Henry Moore | Monitor | 180.0 |
| Jack Anderson | Monitor | 180.0 |
| Emma Davis | Headphones | 165.0 |

*…26 more rows not shown*

---

## 21. Performance Breakdown by customer_name

**Status:** OK

```sql
SELECT
    customer_name,
    COUNT(*) AS transaction_count,
    SUM(unit_cost) AS total_unit_cost,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_cost) AS total_total_cost,
    SUM(total_revenue) AS total_total_revenue,
    SUM(profit) AS total_profit,
    ROUND(AVG(margin_pct), 2) AS avg_margin_pct
FROM data
GROUP BY customer_name
ORDER BY total_profit DESC;
```

**Rows returned:** 11

| customer_name | transaction_count | total_unit_cost | total_unit_price | total_quantity | total_total_cost | total_total_revenue | total_profit | avg_margin_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| David Brown | 14 | 2840.0 | 5089.86 | 109 | 22346.0 | 39778.91 | 17432.91 | 52.18 |
| Isabella Taylor | 12 | 3259.5 | 5739.88 | 98 | 25252.0 | 44469.020000000004 | 16767.09 | 50.07 |
| Bob Smith | 16 | 4200.5 | 7049.84 | 90 | 24144.5 | 40459.09 | 16314.59 | 50.85 |
| Grace Wilson | 11 | 1917.5 | 3419.89 | 69 | 12704.0 | 22709.31 | 10005.31 | 56.71 |
| Alice Johnson | 10 | 3378.0 | 5369.9 | 43 | 12920.0 | 20659.57 | 7739.57 | 51.17 |
| Emma Davis | 12 | 1735.0 | 3079.88 | 65 | 10186.0 | 17649.35 | 7463.35 | 60.44 |
| Frank Miller | 7 | 1533.5 | 2519.93 | 39 | 9822.5 | 16209.61 | 6387.11 | 56.96 |
| Henry Moore | 7 | 1024.0 | 1889.93 | 45 | 6313.0 | 11479.550000000001 | 5166.55 | 57.89 |
| Carol White | 6 | 783.5 | 1579.94 | 39 | 4523.0 | 9289.61 | 4766.610000000001 | 54.9 |
| Jack Anderson | 4 | 913.0 | 1579.96 | 10 | 2379.0 | 4039.8999999999996 | 1660.9 | 52.98 |
| None | 1 | 180.0 | 349.99 | 5 | 900.0 | 1749.95 | 849.95 | 48.6 |

---

## 22. Performance Breakdown by product_name

**Status:** OK

```sql
SELECT
    product_name,
    COUNT(*) AS transaction_count,
    SUM(unit_cost) AS total_unit_cost,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_cost) AS total_total_cost,
    SUM(total_revenue) AS total_total_revenue,
    SUM(profit) AS total_profit,
    ROUND(AVG(margin_pct), 2) AS avg_margin_pct
FROM data
GROUP BY product_name
ORDER BY total_profit DESC;
```

**Rows returned:** 6

| product_name | transaction_count | total_unit_cost | total_unit_price | total_quantity | total_total_cost | total_total_revenue | total_profit | avg_margin_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Laptop | 24 | 15600.0 | 23999.760000000002 | 143 | 92950.0 | 142998.57 | 50048.57 | 35.0 |
| Monitor | 27 | 4680.0 | 9449.73 | 171 | 29520.0 | 59848.29 | 27878.36 | 48.6 |
| Headphones | 15 | 825.0 | 2249.8500000000004 | 89 | 4895.0 | 13349.11 | 8454.11 | 63.3 |
| Keyboard | 19 | 532.0 | 1519.81 | 119 | 3360.0 | 9598.8 | 6238.8 | 65.0 |
| Mouse | 14 | 119.0 | 419.85999999999996 | 82 | 697.0 | 2459.18 | 1762.1799999999998 | 71.7 |
| Mousse | 1 | 8.5 | 29.99 | 8 | 68.0 | 239.92 | 171.92 | 71.7 |

---

## 23. Performance Breakdown by store_name

**Status:** OK

```sql
SELECT
    store_name,
    COUNT(*) AS transaction_count,
    SUM(unit_cost) AS total_unit_cost,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_cost) AS total_total_cost,
    SUM(total_revenue) AS total_total_revenue,
    SUM(profit) AS total_profit,
    ROUND(AVG(margin_pct), 2) AS avg_margin_pct
FROM data
GROUP BY store_name
ORDER BY total_profit DESC;
```

**Rows returned:** 3

| store_name | transaction_count | total_unit_cost | total_unit_price | total_quantity | total_total_cost | total_total_revenue | total_profit | avg_margin_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Store Gamma | 37 | 10177.0 | 16789.63 | 254 | 72851.5 | 119797.45 | 46945.95 | 51.91 |
| Store Beta | 34 | 6322.5 | 11249.66 | 195 | 32758.5 | 59428.05 | 26669.55 | 55.47 |
| Store Alpha | 29 | 5265.0 | 9629.710000000001 | 163 | 25880.0 | 49268.37 | 20938.44 | 55.15 |

---

## 24. customer_name × product_name Performance Matrix

**Status:** ERROR

```sql
SELECT
    customer_name,
    product_name,
    COUNT(*) AS transaction_count,
    SUM(unit_cost) AS total_unit_cost,
    SUM(unit_price) AS total_unit_price,
    SUM(quantity) AS total_quantity,
    SUM(total_cost) AS total_total_cost,
    ROUND(AVG(margin_pct), 2) AS avg_margin_pct
FROM data
GROUP BY customer_name, product_name
ORDER BY total_profit DESC;
```

**Error:** `no such column: total_profit`

---

## 25. Unique order_id Count by customer_name

**Status:** OK

```sql
SELECT
    customer_name,
    COUNT(DISTINCT order_id) AS unique_order_id,
    COUNT(*) AS transaction_count,
    SUM(profit) AS total_profit
FROM data
GROUP BY customer_name
ORDER BY unique_order_id DESC;
```

**Rows returned:** 11

| customer_name | unique_order_id | transaction_count | total_profit |
| --- | --- | --- | --- |
| Bob Smith | 16 | 16 | 16314.59 |
| David Brown | 13 | 14 | 17432.91 |
| Isabella Taylor | 12 | 12 | 16767.09 |
| Emma Davis | 12 | 12 | 7463.35 |
| Grace Wilson | 11 | 11 | 10005.31 |
| Alice Johnson | 10 | 10 | 7739.57 |
| Henry Moore | 7 | 7 | 5166.55 |
| Frank Miller | 7 | 7 | 6387.11 |
| Carol White | 6 | 6 | 4766.610000000001 |
| Jack Anderson | 4 | 4 | 1660.9 |
| None | 1 | 1 | 849.95 |

---

## 26. Unique order_id Count by product_name

**Status:** OK

```sql
SELECT
    product_name,
    COUNT(DISTINCT order_id) AS unique_order_id,
    COUNT(*) AS transaction_count,
    SUM(profit) AS total_profit
FROM data
GROUP BY product_name
ORDER BY unique_order_id DESC;
```

**Rows returned:** 6

| product_name | unique_order_id | transaction_count | total_profit |
| --- | --- | --- | --- |
| Monitor | 26 | 27 | 27878.36 |
| Laptop | 24 | 24 | 50048.57 |
| Keyboard | 19 | 19 | 6238.8 |
| Headphones | 15 | 15 | 8454.11 |
| Mouse | 14 | 14 | 1762.1799999999998 |
| Mousse | 1 | 1 | 171.92 |

---

## 27. Filter by customer_name

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE customer_name = :customer_name;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 28. Total unit_cost for a Specific customer_name

**Status:** SKIPPED

```sql
SELECT customer_name, SUM(unit_cost) AS total_unit_cost
FROM data
WHERE customer_name = :customer_name
GROUP BY customer_name;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 29. Missing Values per Column

**Status:** OK

```sql
SELECT 'order_id' AS column_name, COUNT(*) AS null_count FROM data WHERE order_id IS NULL
UNION ALL
SELECT 'date' AS column_name, COUNT(*) AS null_count FROM data WHERE date IS NULL
UNION ALL
SELECT 'customer_id' AS column_name, COUNT(*) AS null_count FROM data WHERE customer_id IS NULL
UNION ALL
SELECT 'customer_name' AS column_name, COUNT(*) AS null_count FROM data WHERE customer_name IS NULL
UNION ALL
SELECT 'product_id' AS column_name, COUNT(*) AS null_count FROM data WHERE product_id IS NULL
UNION ALL
SELECT 'product_name' AS column_name, COUNT(*) AS null_count FROM data WHERE product_name IS NULL
UNION ALL
SELECT 'unit_cost' AS column_name, COUNT(*) AS null_count FROM data WHERE unit_cost IS NULL
UNION ALL
SELECT 'unit_price' AS column_name, COUNT(*) AS null_count FROM data WHERE unit_price IS NULL
UNION ALL
SELECT 'quantity' AS column_name, COUNT(*) AS null_count FROM data WHERE quantity IS NULL
UNION ALL
SELECT 'total_cost' AS column_name, COUNT(*) AS null_count FROM data WHERE total_cost IS NULL
UNION ALL
SELECT 'total_revenue' AS column_name, COUNT(*) AS null_count FROM data WHERE total_revenue IS NULL
UNION ALL
SELECT 'profit' AS column_name, COUNT(*) AS null_count FROM data WHERE profit IS NULL
ORDER BY null_count DESC;
```

**Rows returned:** 12

| column_name | null_count |
| --- | --- |
| total_cost | 2 |
| profit | 2 |
| customer_id | 1 |
| customer_name | 1 |
| unit_cost | 1 |
| total_revenue | 1 |
| order_id | 0 |
| date | 0 |
| product_id | 0 |
| product_name | 0 |
| unit_price | 0 |
| quantity | 0 |

---

## 30. Duplicate order_id Values

**Status:** OK

```sql
SELECT order_id, COUNT(*) AS occurrences
FROM data
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
```

**Rows returned:** 1

| order_id | occurrences |
| --- | --- |
| ORD0039 | 2 |

---

## 31. Negative unit_cost Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE unit_cost < 0
ORDER BY unit_cost;
```

**Rows returned:** 0

*(no rows returned)*

---

## 32. Negative unit_price Values

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

## 33. Negative quantity Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE quantity < 0
ORDER BY quantity;
```

**Rows returned:** 1

| order_id | date | customer_id | customer_name | product_id | product_name | unit_cost | unit_price | quantity | total_cost | total_revenue | profit | margin_pct | store_id | store_name | city | payment_method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORD0056 | 2025-03-30 | C02 | Bob Smith | P003 | Keyboard | 28.0 | 79.99 | -1 | None | None | None | None | S3 | Store Gamma | Chicago | Debit Card |

---
