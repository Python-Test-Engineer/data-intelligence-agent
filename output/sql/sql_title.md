# SQL Query Catalog — data.csv

Dataset: `data\data.csv`
Columns: `ORDERNUMBER`, `QUANTITYORDERED`, `PRICEEACH`, `ORDERLINENUMBER`, `SALES`, `ORDERDATE`, `STATUS`, `QTR_ID`, `MONTH_ID`, `YEAR_ID`, `PRODUCTLINE`, `MSRP`, `PRODUCTCODE`, `CUSTOMERNAME`, `PHONE`, `ADDRESSLINE1`, `ADDRESSLINE2`, `CITY`, `STATE`, `POSTALCODE`, `COUNTRY`, `TERRITORY`, `CONTACTLASTNAME`, `CONTACTFIRSTNAME`, `DEALSIZE`

---

## Overview

1. Row Count — Returns the total number of rows in the dataset.
2. Column Sample — Returns the first 10 rows to preview the dataset structure.

---

## Numeric Summaries

3. Summary Stats for ORDERNUMBER — Returns min, max, average, and total for ORDERNUMBER.
4. Summary Stats for QUANTITYORDERED — Returns min, max, average, and total for QUANTITYORDERED.
5. Summary Stats for PRICEEACH — Returns min, max, average, and total for PRICEEACH.
6. Summary Stats for ORDERLINENUMBER — Returns min, max, average, and total for ORDERLINENUMBER.
7. Summary Stats for SALES — Returns min, max, average, and total for SALES.
8. Summary Stats for MSRP — Returns min, max, average, and total for MSRP.
9. Total ORDERNUMBER by STATUS — Ranks each STATUS by total ORDERNUMBER, highest first.
10. Average ORDERNUMBER by STATUS — Compares average ORDERNUMBER across each STATUS.
11. Total QUANTITYORDERED by STATUS — Ranks each STATUS by total QUANTITYORDERED, highest first.

---

## Categorical Distributions

12. Distribution of STATUS — Counts rows for each distinct value of STATUS, ordered by frequency.
13. Distribution of PRODUCTLINE — Counts rows for each distinct value of PRODUCTLINE, ordered by frequency.
14. Distribution of ADDRESSLINE2 — Counts rows for each distinct value of ADDRESSLINE2, ordered by frequency.
15. Distribution of STATE — Counts rows for each distinct value of STATE, ordered by frequency.
16. Distribution of COUNTRY — Counts rows for each distinct value of COUNTRY, ordered by frequency.

---

## Rankings

17. ORDERDATE Ranked by Total SALES — Ranks each ORDERDATE by total SALES, highest first.
18. ORDERDATE Ranked by Total QUANTITYORDERED — Ranks each ORDERDATE by total QUANTITYORDERED, highest first.
19. STATUS Ranked by Total SALES — Ranks each STATUS by total SALES, highest first.
20. STATUS Ranked by Total QUANTITYORDERED — Ranks each STATUS by total QUANTITYORDERED, highest first.
21. PRODUCTLINE Ranked by Total SALES — Ranks each PRODUCTLINE by total SALES, highest first.
22. PRODUCTLINE Ranked by Total QUANTITYORDERED — Ranks each PRODUCTLINE by total QUANTITYORDERED, highest first.
23. PRODUCTCODE Ranked by Total SALES — Ranks each PRODUCTCODE by total SALES, highest first.
24. PRODUCTCODE Ranked by Total QUANTITYORDERED — Ranks each PRODUCTCODE by total QUANTITYORDERED, highest first.
25. CUSTOMERNAME Ranked by Total SALES — Ranks each CUSTOMERNAME by total SALES, highest first.
26. CUSTOMERNAME Ranked by Total QUANTITYORDERED — Ranks each CUSTOMERNAME by total QUANTITYORDERED, highest first.
27. PHONE Ranked by Total SALES — Ranks each PHONE by total SALES, highest first.
28. PHONE Ranked by Total QUANTITYORDERED — Ranks each PHONE by total QUANTITYORDERED, highest first.

---

## Multi-Dimensional

29. ORDERNUMBER by STATUS and PRODUCTLINE — Shows total ORDERNUMBER broken down by both STATUS and PRODUCTLINE.

---

## Multi-Metric Analysis

30. Performance Breakdown by STATUS — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by STATUS.
31. Performance Breakdown by PRODUCTLINE — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by PRODUCTLINE.
32. Performance Breakdown by ADDRESSLINE2 — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by ADDRESSLINE2.
33. STATUS × PRODUCTLINE Performance Matrix — Shows performance metrics for every STATUS and PRODUCTLINE combination, ordered by profitability.
34. Unique QTR_ID Count by STATUS — Counts distinct QTR_ID values and key metrics per STATUS to reveal concentration.
35. Unique QTR_ID Count by PRODUCTLINE — Counts distinct QTR_ID values and key metrics per PRODUCTLINE to reveal concentration.

---

## Parametric Lookups

36. Filter by ORDERDATE — Returns all rows where ORDERDATE matches a given value.
37. Performance Summary for a Specific ORDERDATE — Returns transaction count and all key metrics for a single ORDERDATE value.
38. STATUS Breakdown for ORDERDATE = :ORDERDATE — Ranks each STATUS by total SALES filtered to a single ORDERDATE value.
39. PRODUCTLINE Breakdown for ORDERDATE = :ORDERDATE — Ranks each PRODUCTLINE by total SALES filtered to a single ORDERDATE value.
40. Filter by STATUS — Returns all rows where STATUS matches a given value.
41. Performance Summary for a Specific STATUS — Returns transaction count and all key metrics for a single STATUS value.
42. ORDERDATE Breakdown for STATUS = :STATUS — Ranks each ORDERDATE by total SALES filtered to a single STATUS value.
43. PRODUCTLINE Breakdown for STATUS = :STATUS — Ranks each PRODUCTLINE by total SALES filtered to a single STATUS value.
44. Filter by PRODUCTLINE — Returns all rows where PRODUCTLINE matches a given value.
45. Performance Summary for a Specific PRODUCTLINE — Returns transaction count and all key metrics for a single PRODUCTLINE value.
46. ORDERDATE Breakdown for PRODUCTLINE = :PRODUCTLINE — Ranks each ORDERDATE by total SALES filtered to a single PRODUCTLINE value.
47. STATUS Breakdown for PRODUCTLINE = :PRODUCTLINE — Ranks each STATUS by total SALES filtered to a single PRODUCTLINE value.
48. Filter by PRODUCTCODE — Returns all rows where PRODUCTCODE matches a given value.
49. Performance Summary for a Specific PRODUCTCODE — Returns transaction count and all key metrics for a single PRODUCTCODE value.
50. ORDERDATE Breakdown for PRODUCTCODE = :PRODUCTCODE — Ranks each ORDERDATE by total SALES filtered to a single PRODUCTCODE value.
51. STATUS Breakdown for PRODUCTCODE = :PRODUCTCODE — Ranks each STATUS by total SALES filtered to a single PRODUCTCODE value.
52. Filter by CUSTOMERNAME — Returns all rows where CUSTOMERNAME matches a given value.
53. Performance Summary for a Specific CUSTOMERNAME — Returns transaction count and all key metrics for a single CUSTOMERNAME value.
54. ORDERDATE Breakdown for CUSTOMERNAME = :CUSTOMERNAME — Ranks each ORDERDATE by total SALES filtered to a single CUSTOMERNAME value.
55. STATUS Breakdown for CUSTOMERNAME = :CUSTOMERNAME — Ranks each STATUS by total SALES filtered to a single CUSTOMERNAME value.
56. Filter by PHONE — Returns all rows where PHONE matches a given value.
57. Performance Summary for a Specific PHONE — Returns transaction count and all key metrics for a single PHONE value.
58. ORDERDATE Breakdown for PHONE = :PHONE — Ranks each ORDERDATE by total SALES filtered to a single PHONE value.
59. STATUS Breakdown for PHONE = :PHONE — Ranks each STATUS by total SALES filtered to a single PHONE value.
60. Filter by ADDRESSLINE1 — Returns all rows where ADDRESSLINE1 matches a given value.
61. Performance Summary for a Specific ADDRESSLINE1 — Returns transaction count and all key metrics for a single ADDRESSLINE1 value.
62. ORDERDATE Breakdown for ADDRESSLINE1 = :ADDRESSLINE1 — Ranks each ORDERDATE by total SALES filtered to a single ADDRESSLINE1 value.
63. STATUS Breakdown for ADDRESSLINE1 = :ADDRESSLINE1 — Ranks each STATUS by total SALES filtered to a single ADDRESSLINE1 value.
64. Filter by ADDRESSLINE2 — Returns all rows where ADDRESSLINE2 matches a given value.
65. Performance Summary for a Specific ADDRESSLINE2 — Returns transaction count and all key metrics for a single ADDRESSLINE2 value.
66. ORDERDATE Breakdown for ADDRESSLINE2 = :ADDRESSLINE2 — Ranks each ORDERDATE by total SALES filtered to a single ADDRESSLINE2 value.
67. STATUS Breakdown for ADDRESSLINE2 = :ADDRESSLINE2 — Ranks each STATUS by total SALES filtered to a single ADDRESSLINE2 value.
68. Filter by CITY — Returns all rows where CITY matches a given value.
69. Performance Summary for a Specific CITY — Returns transaction count and all key metrics for a single CITY value.
70. ORDERDATE Breakdown for CITY = :CITY — Ranks each ORDERDATE by total SALES filtered to a single CITY value.
71. STATUS Breakdown for CITY = :CITY — Ranks each STATUS by total SALES filtered to a single CITY value.
72. Filter by STATE — Returns all rows where STATE matches a given value.
73. Performance Summary for a Specific STATE — Returns transaction count and all key metrics for a single STATE value.
74. ORDERDATE Breakdown for STATE = :STATE — Ranks each ORDERDATE by total SALES filtered to a single STATE value.
75. STATUS Breakdown for STATE = :STATE — Ranks each STATUS by total SALES filtered to a single STATE value.
76. Filter by POSTALCODE — Returns all rows where POSTALCODE matches a given value.
77. Performance Summary for a Specific POSTALCODE — Returns transaction count and all key metrics for a single POSTALCODE value.
78. ORDERDATE Breakdown for POSTALCODE = :POSTALCODE — Ranks each ORDERDATE by total SALES filtered to a single POSTALCODE value.
79. STATUS Breakdown for POSTALCODE = :POSTALCODE — Ranks each STATUS by total SALES filtered to a single POSTALCODE value.
80. Filter by COUNTRY — Returns all rows where COUNTRY matches a given value.
81. Performance Summary for a Specific COUNTRY — Returns transaction count and all key metrics for a single COUNTRY value.
82. ORDERDATE Breakdown for COUNTRY = :COUNTRY — Ranks each ORDERDATE by total SALES filtered to a single COUNTRY value.
83. STATUS Breakdown for COUNTRY = :COUNTRY — Ranks each STATUS by total SALES filtered to a single COUNTRY value.
84. Filter by TERRITORY — Returns all rows where TERRITORY matches a given value.
85. Performance Summary for a Specific TERRITORY — Returns transaction count and all key metrics for a single TERRITORY value.
86. ORDERDATE Breakdown for TERRITORY = :TERRITORY — Ranks each ORDERDATE by total SALES filtered to a single TERRITORY value.
87. STATUS Breakdown for TERRITORY = :TERRITORY — Ranks each STATUS by total SALES filtered to a single TERRITORY value.
88. Filter by CONTACTLASTNAME — Returns all rows where CONTACTLASTNAME matches a given value.
89. Performance Summary for a Specific CONTACTLASTNAME — Returns transaction count and all key metrics for a single CONTACTLASTNAME value.
90. ORDERDATE Breakdown for CONTACTLASTNAME = :CONTACTLASTNAME — Ranks each ORDERDATE by total SALES filtered to a single CONTACTLASTNAME value.
91. STATUS Breakdown for CONTACTLASTNAME = :CONTACTLASTNAME — Ranks each STATUS by total SALES filtered to a single CONTACTLASTNAME value.
92. Filter by CONTACTFIRSTNAME — Returns all rows where CONTACTFIRSTNAME matches a given value.
93. Performance Summary for a Specific CONTACTFIRSTNAME — Returns transaction count and all key metrics for a single CONTACTFIRSTNAME value.
94. ORDERDATE Breakdown for CONTACTFIRSTNAME = :CONTACTFIRSTNAME — Ranks each ORDERDATE by total SALES filtered to a single CONTACTFIRSTNAME value.
95. STATUS Breakdown for CONTACTFIRSTNAME = :CONTACTFIRSTNAME — Ranks each STATUS by total SALES filtered to a single CONTACTFIRSTNAME value.
96. Filter by DEALSIZE — Returns all rows where DEALSIZE matches a given value.
97. Performance Summary for a Specific DEALSIZE — Returns transaction count and all key metrics for a single DEALSIZE value.
98. ORDERDATE Breakdown for DEALSIZE = :DEALSIZE — Ranks each ORDERDATE by total SALES filtered to a single DEALSIZE value.
99. STATUS Breakdown for DEALSIZE = :DEALSIZE — Ranks each STATUS by total SALES filtered to a single DEALSIZE value.
100. Rows Where SALES Exceeds :min_value — Returns all rows where SALES is above a given threshold.
101. ORDERDATE with Total SALES Above :threshold — Lists ORDERDATE values whose total SALES exceeds a given threshold.

---

## Data Quality Checks

102. Missing Values per Column — Counts NULL values in each column to identify data gaps.
103. Duplicate QTR_ID Values — Flags any QTR_ID that appears more than once in the dataset.
104. Negative ORDERNUMBER Values — Flags rows where ORDERNUMBER is negative, which may indicate data errors.
105. Negative QUANTITYORDERED Values — Flags rows where QUANTITYORDERED is negative, which may indicate data errors.
106. Negative PRICEEACH Values — Flags rows where PRICEEACH is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (2823 rows, 25 columns)*