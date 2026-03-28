# SQL Test Results

Created: `2026-03-28 01:49:19`  
Original CSV: `sales_data_sample.csv`  

Queries file: `C:\Users\mrcra\Desktop\data-intelligence-agent\output\sql\sql_queries_data.md`  
Source CSV: `data\data.csv` (in-memory SQLite)  
Queries run: **106** (all)

---

**Summary:** 40 passed · 0 failed · 66 skipped

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
| 2823 |

---

## 2. Column Sample

**Status:** OK

```sql
SELECT *
FROM data
LIMIT 10;
```

**Rows returned:** 10

| ORDERNUMBER | QUANTITYORDERED | PRICEEACH | ORDERLINENUMBER | SALES | ORDERDATE | STATUS | QTR_ID | MONTH_ID | YEAR_ID | PRODUCTLINE | MSRP | PRODUCTCODE | CUSTOMERNAME | PHONE | ADDRESSLINE1 | ADDRESSLINE2 | CITY | STATE | POSTALCODE | COUNTRY | TERRITORY | CONTACTLASTNAME | CONTACTFIRSTNAME | DEALSIZE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10107 | 30 | 95.7 | 2 | 2871.0 | 2/24/2003 0:00 | Shipped | 1 | 2 | 2003 | Motorcycles | 95 | S10_1678 | Land of Toys Inc. | 2125557818 | 897 Long Airport Avenue | None | NYC | NY | 10022 | USA | None | Yu | Kwai | Small |
| 10121 | 34 | 81.35 | 5 | 2765.9 | 5/7/2003 0:00 | Shipped | 2 | 5 | 2003 | Motorcycles | 95 | S10_1678 | Reims Collectables | 26.47.1555 | 59 rue de l'Abbaye | None | Reims | None | 51100 | France | EMEA | Henriot | Paul | Small |
| 10134 | 41 | 94.74 | 2 | 3884.34 | 7/1/2003 0:00 | Shipped | 3 | 7 | 2003 | Motorcycles | 95 | S10_1678 | Lyon Souveniers | +33 1 46 62 7555 | 27 rue du Colonel Pierre Avia | None | Paris | None | 75508 | France | EMEA | Da Cunha | Daniel | Medium |
| 10145 | 45 | 83.26 | 6 | 3746.7 | 8/25/2003 0:00 | Shipped | 3 | 8 | 2003 | Motorcycles | 95 | S10_1678 | Toys4GrownUps.com | 6265557265 | 78934 Hillside Dr. | None | Pasadena | CA | 90003 | USA | None | Young | Julie | Medium |
| 10159 | 49 | 100.0 | 14 | 5205.27 | 10/10/2003 0:00 | Shipped | 4 | 10 | 2003 | Motorcycles | 95 | S10_1678 | Corporate Gift Ideas Co. | 6505551386 | 7734 Strong St. | None | San Francisco | CA | None | USA | None | Brown | Julie | Medium |
| 10168 | 36 | 96.66 | 1 | 3479.76 | 10/28/2003 0:00 | Shipped | 4 | 10 | 2003 | Motorcycles | 95 | S10_1678 | Technics Stores Inc. | 6505556809 | 9408 Furth Circle | None | Burlingame | CA | 94217 | USA | None | Hirano | Juri | Medium |
| 10180 | 29 | 86.13 | 9 | 2497.77 | 11/11/2003 0:00 | Shipped | 4 | 11 | 2003 | Motorcycles | 95 | S10_1678 | Daedalus Designs Imports | 20.16.1555 | 184, chausse de Tournai | None | Lille | None | 59000 | France | EMEA | Rance | Martine | Small |
| 10188 | 48 | 100.0 | 1 | 5512.32 | 11/18/2003 0:00 | Shipped | 4 | 11 | 2003 | Motorcycles | 95 | S10_1678 | Herkku Gifts | +47 2267 3215 | Drammen 121, PR 744 Sentrum | None | Bergen | None | N 5804 | Norway | EMEA | Oeztan | Veysel | Medium |
| 10201 | 22 | 98.57 | 2 | 2168.54 | 12/1/2003 0:00 | Shipped | 4 | 12 | 2003 | Motorcycles | 95 | S10_1678 | Mini Wheels Co. | 6505555787 | 5557 North Pendale Street | None | San Francisco | CA | None | USA | None | Murphy | Julie | Small |
| 10211 | 41 | 100.0 | 14 | 4708.44 | 1/15/2004 0:00 | Shipped | 1 | 1 | 2004 | Motorcycles | 95 | S10_1678 | Auto Canal Petit | (1) 47.55.6555 | 25, rue Lauriston | None | Paris | None | 75016 | France | EMEA | Perrier | Dominique | Medium |

---

## 3. Summary Stats for ORDERNUMBER

**Status:** OK

```sql
SELECT
    MIN(ORDERNUMBER) AS min_val,
    MAX(ORDERNUMBER) AS max_val,
    ROUND(AVG(ORDERNUMBER), 2) AS avg_val,
    SUM(ORDERNUMBER) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 10100 | 10425 | 10258.73 | 28960381 |

---

## 4. Summary Stats for QUANTITYORDERED

**Status:** OK

```sql
SELECT
    MIN(QUANTITYORDERED) AS min_val,
    MAX(QUANTITYORDERED) AS max_val,
    ROUND(AVG(QUANTITYORDERED), 2) AS avg_val,
    SUM(QUANTITYORDERED) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 6 | 97 | 35.09 | 99067 |

---

## 5. Summary Stats for PRICEEACH

**Status:** OK

```sql
SELECT
    MIN(PRICEEACH) AS min_val,
    MAX(PRICEEACH) AS max_val,
    ROUND(AVG(PRICEEACH), 2) AS avg_val,
    SUM(PRICEEACH) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 26.88 | 100.0 | 83.66 | 236168.07 |

---

## 6. Summary Stats for ORDERLINENUMBER

**Status:** OK

```sql
SELECT
    MIN(ORDERLINENUMBER) AS min_val,
    MAX(ORDERLINENUMBER) AS max_val,
    ROUND(AVG(ORDERLINENUMBER), 2) AS avg_val,
    SUM(ORDERLINENUMBER) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 1 | 18 | 6.47 | 18254 |

---

## 7. Summary Stats for SALES

**Status:** OK

```sql
SELECT
    MIN(SALES) AS min_val,
    MAX(SALES) AS max_val,
    ROUND(AVG(SALES), 2) AS avg_val,
    SUM(SALES) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 482.13 | 14082.8 | 3553.89 | 10032628.85 |

---

## 8. Summary Stats for MSRP

**Status:** OK

```sql
SELECT
    MIN(MSRP) AS min_val,
    MAX(MSRP) AS max_val,
    ROUND(AVG(MSRP), 2) AS avg_val,
    SUM(MSRP) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 33 | 214 | 100.72 | 284320 |

---

## 9. Total ORDERNUMBER by STATUS

**Status:** OK

```sql
SELECT STATUS, SUM(ORDERNUMBER) AS total_ORDERNUMBER
FROM data
GROUP BY STATUS
ORDER BY total_ORDERNUMBER DESC;
```

**Rows returned:** 6

| STATUS | total_ORDERNUMBER |
| --- | --- |
| Shipped | 26830235 |
| Cancelled | 613878 |
| Resolved | 485647 |
| On Hold | 457496 |
| In Process | 427330 |
| Disputed | 145795 |

---

## 10. Average ORDERNUMBER by STATUS

**Status:** OK

```sql
SELECT STATUS, ROUND(AVG(ORDERNUMBER), 2) AS avg_ORDERNUMBER
FROM data
GROUP BY STATUS
ORDER BY avg_ORDERNUMBER DESC;
```

**Rows returned:** 6

| STATUS | avg_ORDERNUMBER |
| --- | --- |
| In Process | 10422.68 |
| Disputed | 10413.93 |
| On Hold | 10397.64 |
| Resolved | 10332.91 |
| Shipped | 10252.29 |
| Cancelled | 10231.3 |

---

## 11. Total QUANTITYORDERED by STATUS

**Status:** OK

```sql
SELECT STATUS, SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
GROUP BY STATUS
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 6

| STATUS | total_QUANTITYORDERED |
| --- | --- |
| Shipped | 91403 |
| Cancelled | 2038 |
| On Hold | 1879 |
| Resolved | 1660 |
| In Process | 1490 |
| Disputed | 597 |

---

## 12. Distribution of STATUS

**Status:** OK

```sql
SELECT STATUS, COUNT(*) AS row_count
FROM data
GROUP BY STATUS
ORDER BY row_count DESC;
```

**Rows returned:** 6

| STATUS | row_count |
| --- | --- |
| Shipped | 2617 |
| Cancelled | 60 |
| Resolved | 47 |
| On Hold | 44 |
| In Process | 41 |
| Disputed | 14 |

---

## 13. Distribution of PRODUCTLINE

**Status:** OK

```sql
SELECT PRODUCTLINE, COUNT(*) AS row_count
FROM data
GROUP BY PRODUCTLINE
ORDER BY row_count DESC;
```

**Rows returned:** 7

| PRODUCTLINE | row_count |
| --- | --- |
| Classic Cars | 967 |
| Vintage Cars | 607 |
| Motorcycles | 331 |
| Planes | 306 |
| Trucks and Buses | 301 |
| Ships | 234 |
| Trains | 77 |

---

## 14. Distribution of ADDRESSLINE2

**Status:** OK

```sql
SELECT ADDRESSLINE2, COUNT(*) AS row_count
FROM data
GROUP BY ADDRESSLINE2
ORDER BY row_count DESC;
```

**Rows returned:** 10

| ADDRESSLINE2 | row_count |
| --- | --- |
| None | 2521 |
| Level 3 | 55 |
| Suite 400 | 48 |
| Level 6 | 46 |
| Level 15 | 46 |
| 2nd Floor | 36 |
| Suite 101 | 25 |
| Suite 750 | 20 |
| Floor No. 4 | 16 |
| Suite 200 | 10 |

---

## 15. Distribution of STATE

**Status:** OK

```sql
SELECT STATE, COUNT(*) AS row_count
FROM data
GROUP BY STATE
ORDER BY row_count DESC;
```

**Rows returned:** 17

| STATE | row_count |
| --- | --- |
| None | 1486 |
| CA | 416 |
| MA | 190 |
| NY | 178 |
| NSW | 92 |
| Victoria | 78 |
| PA | 75 |
| CT | 61 |
| BC | 48 |
| NH | 34 |
| Tokyo | 32 |
| NV | 29 |
| Isle of Wight | 26 |
| Quebec | 22 |
| NJ | 21 |
| Osaka | 20 |
| Queensland | 15 |

---

## 16. Distribution of COUNTRY

**Status:** OK

```sql
SELECT COUNTRY, COUNT(*) AS row_count
FROM data
GROUP BY COUNTRY
ORDER BY row_count DESC;
```

**Rows returned:** 19

| COUNTRY | row_count |
| --- | --- |
| USA | 1004 |
| Spain | 342 |
| France | 314 |
| Australia | 185 |
| UK | 144 |
| Italy | 113 |
| Finland | 92 |
| Norway | 85 |
| Singapore | 79 |
| Canada | 70 |
| Denmark | 63 |
| Germany | 62 |
| Sweden | 57 |
| Austria | 55 |
| Japan | 52 |
| Belgium | 33 |
| Switzerland | 31 |
| Philippines | 26 |
| Ireland | 16 |

---

## 17. ORDERDATE Ranked by Total SALES

**Status:** OK

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Rows returned:** 252

| ORDERDATE | transaction_count | total_SALES |
| --- | --- | --- |
| 11/24/2004 0:00 | 35 | 137644.72 |
| 11/14/2003 0:00 | 38 | 131236.0 |
| 11/6/2003 0:00 | 27 | 114456.85 |
| 11/12/2003 0:00 | 34 | 111156.73 |
| 12/2/2003 0:00 | 28 | 109432.27 |
| 11/5/2004 0:00 | 25 | 106240.69 |
| 11/4/2004 0:00 | 29 | 105074.98 |
| 10/16/2004 0:00 | 28 | 103815.53 |
| 11/17/2004 0:00 | 32 | 97958.38 |
| 10/22/2004 0:00 | 26 | 96850.65 |
| 8/20/2004 0:00 | 27 | 96139.5 |
| 11/20/2003 0:00 | 25 | 95344.63 |
| 9/8/2004 0:00 | 26 | 93717.43 |
| 12/10/2004 0:00 | 24 | 93587.56 |
| 2/17/2005 0:00 | 22 | 92236.97 |
| 11/26/2003 0:00 | 22 | 86508.07 |
| 11/1/2004 0:00 | 26 | 85880.76 |
| 10/14/2004 0:00 | 26 | 85272.92 |
| 11/5/2003 0:00 | 28 | 82140.8 |
| 11/25/2003 0:00 | 21 | 80218.06 |

*…232 more rows not shown*

---

## 18. ORDERDATE Ranked by Total QUANTITYORDERED

**Status:** OK

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(QUANTITYORDERED), 2) AS total_QUANTITYORDERED
FROM data
GROUP BY ORDERDATE
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 252

| ORDERDATE | transaction_count | total_QUANTITYORDERED |
| --- | --- | --- |
| 11/24/2004 0:00 | 35 | 1365.0 |
| 11/14/2003 0:00 | 38 | 1306.0 |
| 11/12/2003 0:00 | 34 | 1093.0 |
| 11/17/2004 0:00 | 32 | 1058.0 |
| 12/2/2003 0:00 | 28 | 1010.0 |
| 11/4/2004 0:00 | 29 | 1002.0 |
| 10/16/2004 0:00 | 28 | 1002.0 |
| 11/6/2003 0:00 | 27 | 977.0 |
| 8/20/2004 0:00 | 27 | 930.0 |
| 11/1/2004 0:00 | 26 | 928.0 |
| 9/8/2004 0:00 | 26 | 909.0 |
| 11/20/2003 0:00 | 25 | 902.0 |
| 11/5/2003 0:00 | 28 | 888.0 |
| 11/5/2004 0:00 | 25 | 877.0 |
| 12/10/2004 0:00 | 24 | 875.0 |
| 10/22/2004 0:00 | 26 | 872.0 |
| 10/14/2004 0:00 | 26 | 864.0 |
| 11/26/2003 0:00 | 22 | 819.0 |
| 11/25/2003 0:00 | 21 | 781.0 |
| 2/17/2005 0:00 | 22 | 768.0 |

*…232 more rows not shown*

---

## 19. STATUS Ranked by Total SALES

**Status:** OK

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Rows returned:** 6

| STATUS | transaction_count | total_SALES |
| --- | --- | --- |
| Shipped | 2617 | 9291501.08 |
| Cancelled | 60 | 194487.48 |
| On Hold | 44 | 178979.19 |
| Resolved | 47 | 150718.28 |
| In Process | 41 | 144729.96 |
| Disputed | 14 | 72212.86 |

---

## 20. STATUS Ranked by Total QUANTITYORDERED

**Status:** OK

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(QUANTITYORDERED), 2) AS total_QUANTITYORDERED
FROM data
GROUP BY STATUS
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 6

| STATUS | transaction_count | total_QUANTITYORDERED |
| --- | --- | --- |
| Shipped | 2617 | 91403.0 |
| Cancelled | 60 | 2038.0 |
| On Hold | 44 | 1879.0 |
| Resolved | 47 | 1660.0 |
| In Process | 41 | 1490.0 |
| Disputed | 14 | 597.0 |

---

## 21. PRODUCTLINE Ranked by Total SALES

**Status:** OK

```sql
SELECT
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY PRODUCTLINE
ORDER BY total_SALES DESC;
```

**Rows returned:** 7

| PRODUCTLINE | transaction_count | total_SALES |
| --- | --- | --- |
| Classic Cars | 967 | 3919615.66 |
| Vintage Cars | 607 | 1903150.84 |
| Motorcycles | 331 | 1166388.34 |
| Trucks and Buses | 301 | 1127789.84 |
| Planes | 306 | 975003.57 |
| Ships | 234 | 714437.13 |
| Trains | 77 | 226243.47 |

---

## 22. PRODUCTLINE Ranked by Total QUANTITYORDERED

**Status:** OK

```sql
SELECT
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(QUANTITYORDERED), 2) AS total_QUANTITYORDERED
FROM data
GROUP BY PRODUCTLINE
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 7

| PRODUCTLINE | transaction_count | total_QUANTITYORDERED |
| --- | --- | --- |
| Classic Cars | 967 | 33992.0 |
| Vintage Cars | 607 | 21069.0 |
| Motorcycles | 331 | 11663.0 |
| Trucks and Buses | 301 | 10777.0 |
| Planes | 306 | 10727.0 |
| Ships | 234 | 8127.0 |
| Trains | 77 | 2712.0 |

---

## 23. PRODUCTCODE Ranked by Total SALES

**Status:** OK

```sql
SELECT
    PRODUCTCODE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY PRODUCTCODE
ORDER BY total_SALES DESC;
```

**Rows returned:** 109

| PRODUCTCODE | transaction_count | total_SALES |
| --- | --- | --- |
| S18_3232 | 52 | 288245.42 |
| S10_1949 | 28 | 191073.03 |
| S10_4698 | 26 | 170401.07 |
| S12_1108 | 26 | 168585.32 |
| S18_2238 | 27 | 154623.95 |
| S12_3891 | 26 | 145332.04 |
| S24_3856 | 27 | 140626.9 |
| S12_2823 | 26 | 140006.16 |
| S18_1662 | 26 | 139421.97 |
| S12_1099 | 25 | 137177.01 |
| S12_1666 | 28 | 136692.72 |
| S18_4027 | 26 | 133779.35 |
| S18_1129 | 27 | 129757.49 |
| S18_3685 | 25 | 128318.05 |
| S10_4962 | 28 | 127548.16 |
| S18_1749 | 22 | 127310.42 |
| S12_3148 | 25 | 125449.75 |
| S24_2300 | 27 | 125273.43 |
| S18_2795 | 26 | 125199.3 |
| S18_4600 | 27 | 123723.08 |

*…89 more rows not shown*

---

## 24. PRODUCTCODE Ranked by Total QUANTITYORDERED

**Status:** OK

```sql
SELECT
    PRODUCTCODE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(QUANTITYORDERED), 2) AS total_QUANTITYORDERED
FROM data
GROUP BY PRODUCTCODE
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 109

| PRODUCTCODE | transaction_count | total_QUANTITYORDERED |
| --- | --- | --- |
| S18_3232 | 52 | 1774.0 |
| S24_3856 | 27 | 1052.0 |
| S18_4600 | 27 | 1031.0 |
| S700_4002 | 27 | 1029.0 |
| S12_4473 | 27 | 1024.0 |
| S24_3949 | 27 | 1008.0 |
| S50_1341 | 26 | 999.0 |
| S18_1097 | 28 | 999.0 |
| S18_2432 | 28 | 998.0 |
| S18_3856 | 26 | 997.0 |
| S18_1342 | 26 | 997.0 |
| S24_2300 | 27 | 996.0 |
| S18_2319 | 26 | 993.0 |
| S18_2949 | 27 | 991.0 |
| S700_2610 | 26 | 990.0 |
| S24_2840 | 28 | 983.0 |
| S50_1392 | 28 | 979.0 |
| S700_2824 | 27 | 976.0 |
| S24_1444 | 28 | 976.0 |
| S12_1108 | 26 | 973.0 |

*…89 more rows not shown*

---

## 25. CUSTOMERNAME Ranked by Total SALES

**Status:** OK

```sql
SELECT
    CUSTOMERNAME,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY CUSTOMERNAME
ORDER BY total_SALES DESC;
```

**Rows returned:** 92

| CUSTOMERNAME | transaction_count | total_SALES |
| --- | --- | --- |
| Euro Shopping Channel | 259 | 912294.11 |
| Mini Gifts Distributors Ltd. | 180 | 654858.06 |
| Australian Collectors, Co. | 55 | 200995.41 |
| Muscle Machine Inc | 48 | 197736.94 |
| La Rochelle Gifts | 53 | 180124.9 |
| Dragon Souveniers, Ltd. | 43 | 172989.68 |
| Land of Toys Inc. | 49 | 164069.44 |
| The Sharp Gifts Warehouse | 40 | 160010.27 |
| AV Stores, Co. | 51 | 157807.81 |
| Anna's Decorations, Ltd | 46 | 153996.13 |
| Souveniers And Things Co. | 46 | 151570.98 |
| Corporate Gift Ideas Co. | 41 | 149882.5 |
| Salzburg Collectables | 40 | 149798.63 |
| Danish Wholesale Imports | 36 | 145041.6 |
| Saveley & Henriot, Co. | 41 | 142874.25 |
| L'ordine Souveniers | 39 | 142601.33 |
| Rovelli Gifts | 48 | 137955.72 |
| Reims Collectables | 41 | 135042.94 |
| Scandinavian Gift Ideas | 38 | 134259.33 |
| Online Diecast Creations Co. | 34 | 131685.3 |

*…72 more rows not shown*

---

## 26. CUSTOMERNAME Ranked by Total QUANTITYORDERED

**Status:** OK

```sql
SELECT
    CUSTOMERNAME,
    COUNT(*) AS transaction_count,
    ROUND(SUM(QUANTITYORDERED), 2) AS total_QUANTITYORDERED
FROM data
GROUP BY CUSTOMERNAME
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 92

| CUSTOMERNAME | transaction_count | total_QUANTITYORDERED |
| --- | --- | --- |
| Euro Shopping Channel | 259 | 9327.0 |
| Mini Gifts Distributors Ltd. | 180 | 6366.0 |
| Australian Collectors, Co. | 55 | 1926.0 |
| La Rochelle Gifts | 53 | 1832.0 |
| AV Stores, Co. | 51 | 1778.0 |
| Muscle Machine Inc | 48 | 1775.0 |
| The Sharp Gifts Warehouse | 40 | 1656.0 |
| Rovelli Gifts | 48 | 1650.0 |
| Land of Toys Inc. | 49 | 1631.0 |
| Souveniers And Things Co. | 46 | 1601.0 |
| Dragon Souveniers, Ltd. | 43 | 1524.0 |
| Anna's Decorations, Ltd | 46 | 1469.0 |
| Corporate Gift Ideas Co. | 41 | 1447.0 |
| Salzburg Collectables | 40 | 1442.0 |
| Reims Collectables | 41 | 1433.0 |
| Saveley & Henriot, Co. | 41 | 1428.0 |
| Scandinavian Gift Ideas | 38 | 1359.0 |
| Danish Wholesale Imports | 36 | 1315.0 |
| L'ordine Souveniers | 39 | 1280.0 |
| Online Diecast Creations Co. | 34 | 1248.0 |

*…72 more rows not shown*

---

## 27. PHONE Ranked by Total SALES

**Status:** OK

```sql
SELECT
    PHONE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY PHONE
ORDER BY total_SALES DESC;
```

**Rows returned:** 91

| PHONE | transaction_count | total_SALES |
| --- | --- | --- |
| (91) 555 94 44 | 259 | 912294.11 |
| 4155551450 | 180 | 654858.06 |
| 03 9520 4555 | 55 | 200995.41 |
| 2125557413 | 48 | 197736.94 |
| 6175558555 | 51 | 184658.36 |
| 40.67.8555 | 53 | 180124.9 |
| +65 221 7555 | 43 | 172989.68 |
| 2125557818 | 49 | 164069.44 |
| 4085553659 | 40 | 160010.27 |
| (171) 555-1555 | 51 | 157807.81 |
| 02 9936 8555 | 46 | 153996.13 |
| +61 2 9495 8555 | 46 | 151570.98 |
| 6505551386 | 41 | 149882.5 |
| 6562-9555 | 40 | 149798.63 |
| 31 12 3555 | 36 | 145041.6 |
| 78.32.5555 | 41 | 142874.25 |
| 0522-556555 | 39 | 142601.33 |
| 035-640555 | 48 | 137955.72 |
| 26.47.1555 | 41 | 135042.94 |
| 0695-34 6555 | 38 | 134259.33 |

*…71 more rows not shown*

---

## 28. PHONE Ranked by Total QUANTITYORDERED

**Status:** OK

```sql
SELECT
    PHONE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(QUANTITYORDERED), 2) AS total_QUANTITYORDERED
FROM data
GROUP BY PHONE
ORDER BY total_QUANTITYORDERED DESC;
```

**Rows returned:** 91

| PHONE | transaction_count | total_QUANTITYORDERED |
| --- | --- | --- |
| (91) 555 94 44 | 259 | 9327.0 |
| 4155551450 | 180 | 6366.0 |
| 03 9520 4555 | 55 | 1926.0 |
| 40.67.8555 | 53 | 1832.0 |
| (171) 555-1555 | 51 | 1778.0 |
| 2125557413 | 48 | 1775.0 |
| 6175558555 | 51 | 1771.0 |
| 4085553659 | 40 | 1656.0 |
| 035-640555 | 48 | 1650.0 |
| 2125557818 | 49 | 1631.0 |
| +61 2 9495 8555 | 46 | 1601.0 |
| +65 221 7555 | 43 | 1524.0 |
| 02 9936 8555 | 46 | 1469.0 |
| 6505551386 | 41 | 1447.0 |
| 6562-9555 | 40 | 1442.0 |
| 26.47.1555 | 41 | 1433.0 |
| 78.32.5555 | 41 | 1428.0 |
| 0695-34 6555 | 38 | 1359.0 |
| 31 12 3555 | 36 | 1315.0 |
| 0522-556555 | 39 | 1280.0 |

*…71 more rows not shown*

---

## 29. ORDERNUMBER by STATUS and PRODUCTLINE

**Status:** OK

```sql
SELECT STATUS, PRODUCTLINE, SUM(ORDERNUMBER) AS total_ORDERNUMBER
FROM data
GROUP BY STATUS, PRODUCTLINE
ORDER BY total_ORDERNUMBER DESC;
```

**Rows returned:** 32

| STATUS | PRODUCTLINE | total_ORDERNUMBER |
| --- | --- | --- |
| Shipped | Classic Cars | 9370574 |
| Shipped | Vintage Cars | 5708250 |
| Shipped | Motorcycles | 3322602 |
| Shipped | Trucks and Buses | 2881066 |
| Shipped | Planes | 2780744 |
| Shipped | Ships | 1998007 |
| Shipped | Trains | 768992 |
| Cancelled | Ships | 183844 |
| In Process | Vintage Cars | 166745 |
| Cancelled | Classic Cars | 163957 |
| In Process | Classic Cars | 145913 |
| Cancelled | Vintage Cars | 132970 |
| On Hold | Classic Cars | 124745 |
| Resolved | Planes | 124514 |
| Resolved | Ships | 124278 |
| Cancelled | Planes | 122859 |
| In Process | Trucks and Buses | 114672 |
| Resolved | Vintage Cars | 103505 |
| On Hold | Vintage Cars | 93679 |
| On Hold | Planes | 93609 |

*…12 more rows not shown*

---

## 30. Performance Breakdown by STATUS

**Status:** OK

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    SUM(ORDERNUMBER) AS total_ORDERNUMBER,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED,
    SUM(PRICEEACH) AS total_PRICEEACH,
    SUM(ORDERLINENUMBER) AS total_ORDERLINENUMBER,
    SUM(SALES) AS total_SALES,
    SUM(MSRP) AS total_MSRP
FROM data
GROUP BY STATUS
ORDER BY total_ORDERNUMBER DESC;
```

**Rows returned:** 6

| STATUS | transaction_count | total_ORDERNUMBER | total_QUANTITYORDERED | total_PRICEEACH | total_ORDERLINENUMBER | total_SALES | total_MSRP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Shipped | 2617 | 26830235 | 91403 | 219074.93 | 16890 | 9291501.08 | 264494 |
| Cancelled | 60 | 613878 | 2038 | 5061.69 | 482 | 194487.48 | 5759 |
| Resolved | 47 | 485647 | 1660 | 3753.2400000000002 | 334 | 150718.28 | 4290 |
| On Hold | 44 | 457496 | 1879 | 3773.9900000000002 | 282 | 178979.19 | 4237 |
| In Process | 41 | 427330 | 1490 | 3251.96 | 224 | 144729.96 | 4011 |
| Disputed | 14 | 145795 | 597 | 1252.26 | 42 | 72212.86 | 1529 |

---

## 31. Performance Breakdown by PRODUCTLINE

**Status:** OK

```sql
SELECT
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    SUM(ORDERNUMBER) AS total_ORDERNUMBER,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED,
    SUM(PRICEEACH) AS total_PRICEEACH,
    SUM(ORDERLINENUMBER) AS total_ORDERLINENUMBER,
    SUM(SALES) AS total_SALES,
    SUM(MSRP) AS total_MSRP
FROM data
GROUP BY PRODUCTLINE
ORDER BY total_ORDERNUMBER DESC;
```

**Rows returned:** 7

| PRODUCTLINE | transaction_count | total_ORDERNUMBER | total_QUANTITYORDERED | total_PRICEEACH | total_ORDERLINENUMBER | total_SALES | total_MSRP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Classic Cars | 967 | 9918937 | 33992 | 84453.7 | 6233 | 3919615.66 | 115929 |
| Vintage Cars | 607 | 6225979 | 21069 | 47435.96 | 3834 | 1903150.84 | 52482 |
| Motorcycles | 331 | 3395505 | 11663 | 27472.19 | 1963 | 1166388.34 | 32130 |
| Planes | 306 | 3142556 | 10727 | 25012.72 | 2210 | 975003.57 | 27163 |
| Trucks and Buses | 301 | 3087894 | 10777 | 26345.91 | 1873 | 1127789.84 | 30842 |
| Ships | 234 | 2399856 | 8127 | 19622.18 | 1591 | 714437.13 | 20154 |
| Trains | 77 | 789654 | 2712 | 5825.41 | 550 | 226243.47 | 5620 |

---

## 32. Performance Breakdown by ADDRESSLINE2

**Status:** OK

```sql
SELECT
    ADDRESSLINE2,
    COUNT(*) AS transaction_count,
    SUM(ORDERNUMBER) AS total_ORDERNUMBER,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED,
    SUM(PRICEEACH) AS total_PRICEEACH,
    SUM(ORDERLINENUMBER) AS total_ORDERLINENUMBER,
    SUM(SALES) AS total_SALES,
    SUM(MSRP) AS total_MSRP
FROM data
GROUP BY ADDRESSLINE2
ORDER BY total_ORDERNUMBER DESC;
```

**Rows returned:** 10

| ADDRESSLINE2 | transaction_count | total_ORDERNUMBER | total_QUANTITYORDERED | total_PRICEEACH | total_ORDERLINENUMBER | total_SALES | total_MSRP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| None | 2521 | 25862123 | 88682 | 210813.92 | 16344 | 8956092.84 | 253576 |
| Level 3 | 55 | 563321 | 1926 | 4714.48 | 387 | 200995.41 | 5694 |
| Suite 400 | 48 | 490465 | 1775 | 4104.23 | 349 | 197736.94 | 5203 |
| Level 6 | 46 | 474596 | 1601 | 3810.23 | 298 | 151570.98 | 4282 |
| Level 15 | 46 | 471509 | 1469 | 3843.67 | 296 | 153996.13 | 4817 |
| 2nd Floor | 36 | 369736 | 1236 | 2862.93 | 227 | 115498.73 | 3500 |
| Suite 101 | 25 | 256873 | 787 | 2108.11 | 153 | 88041.26 | 2552 |
| Suite 750 | 20 | 204586 | 720 | 1779.62 | 81 | 77795.2 | 2133 |
| Floor No. 4 | 16 | 164059 | 490 | 1377.98 | 73 | 57756.43 | 1710 |
| Suite 200 | 10 | 103113 | 381 | 752.9 | 46 | 33144.93 | 853 |

---

## 33. STATUS × PRODUCTLINE Performance Matrix

**Status:** OK

```sql
SELECT
    STATUS,
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    SUM(ORDERNUMBER) AS total_ORDERNUMBER,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED,
    SUM(PRICEEACH) AS total_PRICEEACH,
    SUM(ORDERLINENUMBER) AS total_ORDERLINENUMBER
FROM data
GROUP BY STATUS, PRODUCTLINE
ORDER BY total_ORDERNUMBER DESC;
```

**Rows returned:** 32

| STATUS | PRODUCTLINE | transaction_count | total_ORDERNUMBER | total_QUANTITYORDERED | total_PRICEEACH | total_ORDERLINENUMBER |
| --- | --- | --- | --- | --- | --- | --- |
| Shipped | Classic Cars | 914 | 9370574 | 31955 | 79880.25 | 5879 |
| Shipped | Vintage Cars | 557 | 5708250 | 19281 | 43611.33 | 3554 |
| Shipped | Motorcycles | 324 | 3322602 | 11355 | 26811.01 | 1941 |
| Shipped | Trucks and Buses | 281 | 2881066 | 10009 | 24589.87 | 1762 |
| Shipped | Planes | 271 | 2780744 | 9389 | 22292.48 | 1940 |
| Shipped | Ships | 195 | 1998007 | 6792 | 16264.58 | 1292 |
| Shipped | Trains | 75 | 768992 | 2622 | 5625.41 | 522 |
| Cancelled | Ships | 18 | 183844 | 628 | 1522.7 | 178 |
| In Process | Vintage Cars | 16 | 166745 | 532 | 1174.62 | 46 |
| Cancelled | Classic Cars | 16 | 163957 | 493 | 1469.43 | 117 |
| In Process | Classic Cars | 14 | 145913 | 564 | 1136.79 | 106 |
| Cancelled | Vintage Cars | 13 | 132970 | 460 | 1053.07 | 104 |
| On Hold | Classic Cars | 12 | 124745 | 512 | 1044.88 | 80 |
| Resolved | Planes | 12 | 124514 | 442 | 915.4 | 133 |
| Resolved | Ships | 12 | 124278 | 404 | 1061.85 | 59 |
| Cancelled | Planes | 12 | 122859 | 415 | 916.49 | 69 |
| In Process | Trucks and Buses | 11 | 114672 | 394 | 940.55 | 72 |
| Resolved | Vintage Cars | 10 | 103505 | 317 | 699.53 | 74 |
| On Hold | Vintage Cars | 9 | 93679 | 410 | 727.71 | 49 |
| On Hold | Planes | 9 | 93609 | 418 | 762.92 | 64 |

*…12 more rows not shown*

---

## 34. Unique QTR_ID Count by STATUS

**Status:** OK

```sql
SELECT
    STATUS,
    COUNT(DISTINCT QTR_ID) AS unique_QTR_ID,
    COUNT(*) AS transaction_count,
    SUM(ORDERNUMBER) AS total_ORDERNUMBER
FROM data
GROUP BY STATUS
ORDER BY unique_QTR_ID DESC;
```

**Rows returned:** 6

| STATUS | unique_QTR_ID | transaction_count | total_ORDERNUMBER |
| --- | --- | --- | --- |
| Shipped | 4 | 2617 | 26830235 |
| Resolved | 2 | 47 | 485647 |
| On Hold | 2 | 44 | 457496 |
| Cancelled | 2 | 60 | 613878 |
| In Process | 1 | 41 | 427330 |
| Disputed | 1 | 14 | 145795 |

---

## 35. Unique QTR_ID Count by PRODUCTLINE

**Status:** OK

```sql
SELECT
    PRODUCTLINE,
    COUNT(DISTINCT QTR_ID) AS unique_QTR_ID,
    COUNT(*) AS transaction_count,
    SUM(ORDERNUMBER) AS total_ORDERNUMBER
FROM data
GROUP BY PRODUCTLINE
ORDER BY unique_QTR_ID DESC;
```

**Rows returned:** 7

| PRODUCTLINE | unique_QTR_ID | transaction_count | total_ORDERNUMBER |
| --- | --- | --- | --- |
| Vintage Cars | 4 | 607 | 6225979 |
| Trucks and Buses | 4 | 301 | 3087894 |
| Trains | 4 | 77 | 789654 |
| Ships | 4 | 234 | 2399856 |
| Planes | 4 | 306 | 3142556 |
| Motorcycles | 4 | 331 | 3395505 |
| Classic Cars | 4 | 967 | 9918937 |

---

## 36. Filter by ORDERDATE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE ORDERDATE = :ORDERDATE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 37. Performance Summary for a Specific ORDERDATE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE ORDERDATE = :ORDERDATE
GROUP BY ORDERDATE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 38. STATUS Breakdown for ORDERDATE = :ORDERDATE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE ORDERDATE = :ORDERDATE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 39. PRODUCTLINE Breakdown for ORDERDATE = :ORDERDATE

**Status:** SKIPPED

```sql
SELECT
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE ORDERDATE = :ORDERDATE
GROUP BY PRODUCTLINE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 40. Filter by STATUS

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE STATUS = :STATUS;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 41. Performance Summary for a Specific STATUS

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE STATUS = :STATUS
GROUP BY STATUS;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 42. ORDERDATE Breakdown for STATUS = :STATUS

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE STATUS = :STATUS
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 43. PRODUCTLINE Breakdown for STATUS = :STATUS

**Status:** SKIPPED

```sql
SELECT
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE STATUS = :STATUS
GROUP BY PRODUCTLINE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 44. Filter by PRODUCTLINE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE PRODUCTLINE = :PRODUCTLINE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 45. Performance Summary for a Specific PRODUCTLINE

**Status:** SKIPPED

```sql
SELECT
    PRODUCTLINE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE PRODUCTLINE = :PRODUCTLINE
GROUP BY PRODUCTLINE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 46. ORDERDATE Breakdown for PRODUCTLINE = :PRODUCTLINE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE PRODUCTLINE = :PRODUCTLINE
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 47. STATUS Breakdown for PRODUCTLINE = :PRODUCTLINE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE PRODUCTLINE = :PRODUCTLINE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 48. Filter by PRODUCTCODE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE PRODUCTCODE = :PRODUCTCODE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 49. Performance Summary for a Specific PRODUCTCODE

**Status:** SKIPPED

```sql
SELECT
    PRODUCTCODE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE PRODUCTCODE = :PRODUCTCODE
GROUP BY PRODUCTCODE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 50. ORDERDATE Breakdown for PRODUCTCODE = :PRODUCTCODE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE PRODUCTCODE = :PRODUCTCODE
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 51. STATUS Breakdown for PRODUCTCODE = :PRODUCTCODE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE PRODUCTCODE = :PRODUCTCODE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 52. Filter by CUSTOMERNAME

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE CUSTOMERNAME = :CUSTOMERNAME;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 53. Performance Summary for a Specific CUSTOMERNAME

**Status:** SKIPPED

```sql
SELECT
    CUSTOMERNAME,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE CUSTOMERNAME = :CUSTOMERNAME
GROUP BY CUSTOMERNAME;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 54. ORDERDATE Breakdown for CUSTOMERNAME = :CUSTOMERNAME

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CUSTOMERNAME = :CUSTOMERNAME
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 55. STATUS Breakdown for CUSTOMERNAME = :CUSTOMERNAME

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CUSTOMERNAME = :CUSTOMERNAME
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 56. Filter by PHONE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE PHONE = :PHONE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 57. Performance Summary for a Specific PHONE

**Status:** SKIPPED

```sql
SELECT
    PHONE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE PHONE = :PHONE
GROUP BY PHONE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 58. ORDERDATE Breakdown for PHONE = :PHONE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE PHONE = :PHONE
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 59. STATUS Breakdown for PHONE = :PHONE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE PHONE = :PHONE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 60. Filter by ADDRESSLINE1

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE ADDRESSLINE1 = :ADDRESSLINE1;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 61. Performance Summary for a Specific ADDRESSLINE1

**Status:** SKIPPED

```sql
SELECT
    ADDRESSLINE1,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE ADDRESSLINE1 = :ADDRESSLINE1
GROUP BY ADDRESSLINE1;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 62. ORDERDATE Breakdown for ADDRESSLINE1 = :ADDRESSLINE1

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE ADDRESSLINE1 = :ADDRESSLINE1
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 63. STATUS Breakdown for ADDRESSLINE1 = :ADDRESSLINE1

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE ADDRESSLINE1 = :ADDRESSLINE1
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 64. Filter by ADDRESSLINE2

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE ADDRESSLINE2 = :ADDRESSLINE2;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 65. Performance Summary for a Specific ADDRESSLINE2

**Status:** SKIPPED

```sql
SELECT
    ADDRESSLINE2,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE ADDRESSLINE2 = :ADDRESSLINE2
GROUP BY ADDRESSLINE2;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 66. ORDERDATE Breakdown for ADDRESSLINE2 = :ADDRESSLINE2

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE ADDRESSLINE2 = :ADDRESSLINE2
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 67. STATUS Breakdown for ADDRESSLINE2 = :ADDRESSLINE2

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE ADDRESSLINE2 = :ADDRESSLINE2
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 68. Filter by CITY

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE CITY = :CITY;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 69. Performance Summary for a Specific CITY

**Status:** SKIPPED

```sql
SELECT
    CITY,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE CITY = :CITY
GROUP BY CITY;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 70. ORDERDATE Breakdown for CITY = :CITY

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CITY = :CITY
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 71. STATUS Breakdown for CITY = :CITY

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CITY = :CITY
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 72. Filter by STATE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE STATE = :STATE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 73. Performance Summary for a Specific STATE

**Status:** SKIPPED

```sql
SELECT
    STATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE STATE = :STATE
GROUP BY STATE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 74. ORDERDATE Breakdown for STATE = :STATE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE STATE = :STATE
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 75. STATUS Breakdown for STATE = :STATE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE STATE = :STATE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 76. Filter by POSTALCODE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE POSTALCODE = :POSTALCODE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 77. Performance Summary for a Specific POSTALCODE

**Status:** SKIPPED

```sql
SELECT
    POSTALCODE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE POSTALCODE = :POSTALCODE
GROUP BY POSTALCODE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 78. ORDERDATE Breakdown for POSTALCODE = :POSTALCODE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE POSTALCODE = :POSTALCODE
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 79. STATUS Breakdown for POSTALCODE = :POSTALCODE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE POSTALCODE = :POSTALCODE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 80. Filter by COUNTRY

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE COUNTRY = :COUNTRY;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 81. Performance Summary for a Specific COUNTRY

**Status:** SKIPPED

```sql
SELECT
    COUNTRY,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE COUNTRY = :COUNTRY
GROUP BY COUNTRY;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 82. ORDERDATE Breakdown for COUNTRY = :COUNTRY

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE COUNTRY = :COUNTRY
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 83. STATUS Breakdown for COUNTRY = :COUNTRY

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE COUNTRY = :COUNTRY
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 84. Filter by TERRITORY

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE TERRITORY = :TERRITORY;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 85. Performance Summary for a Specific TERRITORY

**Status:** SKIPPED

```sql
SELECT
    TERRITORY,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE TERRITORY = :TERRITORY
GROUP BY TERRITORY;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 86. ORDERDATE Breakdown for TERRITORY = :TERRITORY

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE TERRITORY = :TERRITORY
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 87. STATUS Breakdown for TERRITORY = :TERRITORY

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE TERRITORY = :TERRITORY
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 88. Filter by CONTACTLASTNAME

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE CONTACTLASTNAME = :CONTACTLASTNAME;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 89. Performance Summary for a Specific CONTACTLASTNAME

**Status:** SKIPPED

```sql
SELECT
    CONTACTLASTNAME,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE CONTACTLASTNAME = :CONTACTLASTNAME
GROUP BY CONTACTLASTNAME;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 90. ORDERDATE Breakdown for CONTACTLASTNAME = :CONTACTLASTNAME

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CONTACTLASTNAME = :CONTACTLASTNAME
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 91. STATUS Breakdown for CONTACTLASTNAME = :CONTACTLASTNAME

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CONTACTLASTNAME = :CONTACTLASTNAME
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 92. Filter by CONTACTFIRSTNAME

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE CONTACTFIRSTNAME = :CONTACTFIRSTNAME;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 93. Performance Summary for a Specific CONTACTFIRSTNAME

**Status:** SKIPPED

```sql
SELECT
    CONTACTFIRSTNAME,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE CONTACTFIRSTNAME = :CONTACTFIRSTNAME
GROUP BY CONTACTFIRSTNAME;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 94. ORDERDATE Breakdown for CONTACTFIRSTNAME = :CONTACTFIRSTNAME

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CONTACTFIRSTNAME = :CONTACTFIRSTNAME
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 95. STATUS Breakdown for CONTACTFIRSTNAME = :CONTACTFIRSTNAME

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE CONTACTFIRSTNAME = :CONTACTFIRSTNAME
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 96. Filter by DEALSIZE

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE DEALSIZE = :DEALSIZE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 97. Performance Summary for a Specific DEALSIZE

**Status:** SKIPPED

```sql
SELECT
    DEALSIZE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES,
    SUM(QUANTITYORDERED) AS total_QUANTITYORDERED
FROM data
WHERE DEALSIZE = :DEALSIZE
GROUP BY DEALSIZE;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 98. ORDERDATE Breakdown for DEALSIZE = :DEALSIZE

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE DEALSIZE = :DEALSIZE
GROUP BY ORDERDATE
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 99. STATUS Breakdown for DEALSIZE = :DEALSIZE

**Status:** SKIPPED

```sql
SELECT
    STATUS,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
WHERE DEALSIZE = :DEALSIZE
GROUP BY STATUS
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 100. Rows Where SALES Exceeds :min_value

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE SALES > :min_value
ORDER BY SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 101. ORDERDATE with Total SALES Above :threshold

**Status:** SKIPPED

```sql
SELECT
    ORDERDATE,
    COUNT(*) AS transaction_count,
    ROUND(SUM(SALES), 2) AS total_SALES
FROM data
GROUP BY ORDERDATE
HAVING SUM(SALES) > :threshold
ORDER BY total_SALES DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 102. Missing Values per Column

**Status:** OK

```sql
SELECT 'ORDERNUMBER' AS column_name, COUNT(*) AS null_count FROM data WHERE ORDERNUMBER IS NULL
UNION ALL
SELECT 'QUANTITYORDERED' AS column_name, COUNT(*) AS null_count FROM data WHERE QUANTITYORDERED IS NULL
UNION ALL
SELECT 'PRICEEACH' AS column_name, COUNT(*) AS null_count FROM data WHERE PRICEEACH IS NULL
UNION ALL
SELECT 'ORDERLINENUMBER' AS column_name, COUNT(*) AS null_count FROM data WHERE ORDERLINENUMBER IS NULL
UNION ALL
SELECT 'SALES' AS column_name, COUNT(*) AS null_count FROM data WHERE SALES IS NULL
UNION ALL
SELECT 'ORDERDATE' AS column_name, COUNT(*) AS null_count FROM data WHERE ORDERDATE IS NULL
UNION ALL
SELECT 'STATUS' AS column_name, COUNT(*) AS null_count FROM data WHERE STATUS IS NULL
UNION ALL
SELECT 'QTR_ID' AS column_name, COUNT(*) AS null_count FROM data WHERE QTR_ID IS NULL
UNION ALL
SELECT 'MONTH_ID' AS column_name, COUNT(*) AS null_count FROM data WHERE MONTH_ID IS NULL
UNION ALL
SELECT 'YEAR_ID' AS column_name, COUNT(*) AS null_count FROM data WHERE YEAR_ID IS NULL
UNION ALL
SELECT 'PRODUCTLINE' AS column_name, COUNT(*) AS null_count FROM data WHERE PRODUCTLINE IS NULL
UNION ALL
SELECT 'MSRP' AS column_name, COUNT(*) AS null_count FROM data WHERE MSRP IS NULL
ORDER BY null_count DESC;
```

**Rows returned:** 12

| column_name | null_count |
| --- | --- |
| ORDERNUMBER | 0 |
| QUANTITYORDERED | 0 |
| PRICEEACH | 0 |
| ORDERLINENUMBER | 0 |
| SALES | 0 |
| ORDERDATE | 0 |
| STATUS | 0 |
| QTR_ID | 0 |
| MONTH_ID | 0 |
| YEAR_ID | 0 |
| PRODUCTLINE | 0 |
| MSRP | 0 |

---

## 103. Duplicate QTR_ID Values

**Status:** OK

```sql
SELECT QTR_ID, COUNT(*) AS occurrences
FROM data
GROUP BY QTR_ID
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
```

**Rows returned:** 4

| QTR_ID | occurrences |
| --- | --- |
| 4 | 1094 |
| 1 | 665 |
| 2 | 561 |
| 3 | 503 |

---

## 104. Negative ORDERNUMBER Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE ORDERNUMBER < 0
ORDER BY ORDERNUMBER;
```

**Rows returned:** 0

*(no rows returned)*

---

## 105. Negative QUANTITYORDERED Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE QUANTITYORDERED < 0
ORDER BY QUANTITYORDERED;
```

**Rows returned:** 0

*(no rows returned)*

---

## 106. Negative PRICEEACH Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE PRICEEACH < 0
ORDER BY PRICEEACH;
```

**Rows returned:** 0

*(no rows returned)*

---
