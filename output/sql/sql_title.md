# SQL Query Catalog — data.csv

Dataset: `C:\Users\mrcra\Desktop\data-intelligence-agent\data\data.csv`
Columns: `PatientId`, `AppointmentID`, `Gender`, `ScheduledDay`, `AppointmentDay`, `Age`, `Neighbourhood`, `Scholarship`, `Hipertension`, `Diabetes`, `Alcoholism`, `Handcap`, `SMS_received`, `No-show`

---

## Overview

1. Row Count — Returns the total number of rows in the dataset.
2. Column Sample — Returns the first 10 rows to preview the dataset structure.

---

## Numeric Summaries

3. Summary Stats for PatientId — Returns min, max, average, and total for PatientId.
4. Summary Stats for AppointmentID — Returns min, max, average, and total for AppointmentID.
5. Summary Stats for Age — Returns min, max, average, and total for Age.
6. Summary Stats for Scholarship — Returns min, max, average, and total for Scholarship.
7. Summary Stats for Hipertension — Returns min, max, average, and total for Hipertension.
8. Summary Stats for Diabetes — Returns min, max, average, and total for Diabetes.
9. Total PatientId by Gender — Ranks each Gender by total PatientId, highest first.
10. Average PatientId by Gender — Compares average PatientId across each Gender.
11. Total AppointmentID by Gender — Ranks each Gender by total AppointmentID, highest first.

---

## Categorical Distributions

12. Distribution of Gender — Counts rows for each distinct value of Gender, ordered by frequency.
13. Distribution of AppointmentDay — Counts rows for each distinct value of AppointmentDay, ordered by frequency.
14. Distribution of No-show — Counts rows for each distinct value of No-show, ordered by frequency.

---

## Rankings

15. Top 10 Gender by PatientId — Lists the 10 Gender values with the highest total PatientId.
16. Bottom 10 Gender by PatientId — Lists the 10 Gender values with the lowest total PatientId.
17. Top 10 AppointmentDay by PatientId — Lists the 10 AppointmentDay values with the highest total PatientId.

---

## Multi-Dimensional

18. PatientId by Gender and AppointmentDay — Shows total PatientId broken down by both Gender and AppointmentDay.

---

## Multi-Metric Analysis

19. Performance Breakdown by Gender — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by Gender.
20. Performance Breakdown by AppointmentDay — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by AppointmentDay.
21. Performance Breakdown by No-show — Aggregates transaction count and all key metrics (revenue, cost, profit, margins) grouped by No-show.
22. Gender × AppointmentDay Performance Matrix — Shows performance metrics for every Gender and AppointmentDay combination, ordered by profitability.

---

## Parametric Lookups

23. Filter by Gender — Returns all rows where Gender matches a given value.
24. Performance Summary for a Specific Gender — Returns transaction count and all key metrics for a single Gender value.
25. AppointmentDay Breakdown for Gender = :Gender — Ranks each AppointmentDay by total PatientId filtered to a single Gender value.
26. Neighbourhood Breakdown for Gender = :Gender — Ranks each Neighbourhood by total PatientId filtered to a single Gender value.
27. Filter by AppointmentDay — Returns all rows where AppointmentDay matches a given value.
28. Performance Summary for a Specific AppointmentDay — Returns transaction count and all key metrics for a single AppointmentDay value.
29. Gender Breakdown for AppointmentDay = :AppointmentDay — Ranks each Gender by total PatientId filtered to a single AppointmentDay value.
30. Neighbourhood Breakdown for AppointmentDay = :AppointmentDay — Ranks each Neighbourhood by total PatientId filtered to a single AppointmentDay value.
31. Filter by Neighbourhood — Returns all rows where Neighbourhood matches a given value.
32. Performance Summary for a Specific Neighbourhood — Returns transaction count and all key metrics for a single Neighbourhood value.
33. Gender Breakdown for Neighbourhood = :Neighbourhood — Ranks each Gender by total PatientId filtered to a single Neighbourhood value.
34. AppointmentDay Breakdown for Neighbourhood = :Neighbourhood — Ranks each AppointmentDay by total PatientId filtered to a single Neighbourhood value.
35. Filter by No-show — Returns all rows where No-show matches a given value.
36. Performance Summary for a Specific No-show — Returns transaction count and all key metrics for a single No-show value.
37. Gender Breakdown for No-show = :No-show — Ranks each Gender by total PatientId filtered to a single No-show value.
38. AppointmentDay Breakdown for No-show = :No-show — Ranks each AppointmentDay by total PatientId filtered to a single No-show value.
39. Rows Where PatientId Exceeds :min_value — Returns all rows where PatientId is above a given threshold.
40. Gender with Total PatientId Above :threshold — Lists Gender values whose total PatientId exceeds a given threshold.

---

## Data Quality Checks

41. Missing Values per Column — Counts NULL values in each column to identify data gaps.
42. Negative PatientId Values — Flags rows where PatientId is negative, which may indicate data errors.
43. Negative AppointmentID Values — Flags rows where AppointmentID is negative, which may indicate data errors.
44. Negative Age Values — Flags rows where Age is negative, which may indicate data errors.

---

*Generated from dataset inspection — data.csv (110527 rows, 14 columns)*