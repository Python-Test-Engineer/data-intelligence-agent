# SQL Test Results

Created: `2026-05-14 14:05:36`  
Original CSV: `kaggle_dna.csv`  

Queries file: `C:\Users\mrcra\Desktop\data-intelligence-agent\output\sql\sql_queries_data.md`  
Source CSV: `C:\Users\mrcra\Desktop\data-intelligence-agent\data\data.csv` (in-memory SQLite)  
Queries run: **44** (all)

---

**Summary:** 24 passed · 2 failed · 18 skipped

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
| 110527 |

---

## 2. Column Sample

**Status:** OK

```sql
SELECT *
FROM data
LIMIT 10;
```

**Rows returned:** 10

| PatientId | AppointmentID | Gender | ScheduledDay | AppointmentDay | Age | Neighbourhood | Scholarship | Hipertension | Diabetes | Alcoholism | Handcap | SMS_received | No-show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29872499824296.0 | 5642903 | F | 2016-04-29T18:38:08Z | 2016-04-29T00:00:00Z | 62 | JARDIM DA PENHA | 0 | 1 | 0 | 0 | 0 | 0 | No |
| 558997776694438.0 | 5642503 | M | 2016-04-29T16:08:27Z | 2016-04-29T00:00:00Z | 56 | JARDIM DA PENHA | 0 | 0 | 0 | 0 | 0 | 0 | No |
| 4262962299951.0 | 5642549 | F | 2016-04-29T16:19:04Z | 2016-04-29T00:00:00Z | 62 | MATA DA PRAIA | 0 | 0 | 0 | 0 | 0 | 0 | No |
| 867951213174.0 | 5642828 | F | 2016-04-29T17:29:31Z | 2016-04-29T00:00:00Z | 8 | PONTAL DE CAMBURI | 0 | 0 | 0 | 0 | 0 | 0 | No |
| 8841186448183.0 | 5642494 | F | 2016-04-29T16:07:23Z | 2016-04-29T00:00:00Z | 56 | JARDIM DA PENHA | 0 | 1 | 1 | 0 | 0 | 0 | No |
| 95985133231274.0 | 5626772 | F | 2016-04-27T08:36:51Z | 2016-04-29T00:00:00Z | 76 | REPÚBLICA | 0 | 1 | 0 | 0 | 0 | 0 | No |
| 733688164476661.0 | 5630279 | F | 2016-04-27T15:05:12Z | 2016-04-29T00:00:00Z | 23 | GOIABEIRAS | 0 | 0 | 0 | 0 | 0 | 0 | Yes |
| 3449833394123.0 | 5630575 | F | 2016-04-27T15:39:58Z | 2016-04-29T00:00:00Z | 39 | GOIABEIRAS | 0 | 0 | 0 | 0 | 0 | 0 | Yes |
| 56394729949972.0 | 5638447 | F | 2016-04-29T08:02:16Z | 2016-04-29T00:00:00Z | 21 | ANDORINHAS | 0 | 0 | 0 | 0 | 0 | 0 | No |
| 78124564369297.0 | 5629123 | F | 2016-04-27T12:48:25Z | 2016-04-29T00:00:00Z | 19 | CONQUISTA | 0 | 0 | 0 | 0 | 0 | 0 | No |

---

## 3. Summary Stats for PatientId

**Status:** OK

```sql
SELECT
    MIN(PatientId) AS min_val,
    MAX(PatientId) AS max_val,
    ROUND(AVG(PatientId), 2) AS avg_val,
    SUM(PatientId) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 39217.84439 | 999981631772427.0 | 147496265710394.1 | 1.6302319760172728e+19 |

---

## 4. Summary Stats for AppointmentID

**Status:** OK

```sql
SELECT
    MIN(AppointmentID) AS min_val,
    MAX(AppointmentID) AS max_val,
    ROUND(AVG(AppointmentID), 2) AS avg_val,
    SUM(AppointmentID) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 5030230 | 5790484 | 5675305.12 | 627274449377 |

---

## 5. Summary Stats for Age

**Status:** OK

```sql
SELECT
    MIN(Age) AS min_val,
    MAX(Age) AS max_val,
    ROUND(AVG(Age), 2) AS avg_val,
    SUM(Age) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| -1 | 115 | 37.09 | 4099322 |

---

## 6. Summary Stats for Scholarship

**Status:** OK

```sql
SELECT
    MIN(Scholarship) AS min_val,
    MAX(Scholarship) AS max_val,
    ROUND(AVG(Scholarship), 2) AS avg_val,
    SUM(Scholarship) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 0 | 1 | 0.1 | 10861 |

---

## 7. Summary Stats for Hipertension

**Status:** OK

```sql
SELECT
    MIN(Hipertension) AS min_val,
    MAX(Hipertension) AS max_val,
    ROUND(AVG(Hipertension), 2) AS avg_val,
    SUM(Hipertension) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 0 | 1 | 0.2 | 21801 |

---

## 8. Summary Stats for Diabetes

**Status:** OK

```sql
SELECT
    MIN(Diabetes) AS min_val,
    MAX(Diabetes) AS max_val,
    ROUND(AVG(Diabetes), 2) AS avg_val,
    SUM(Diabetes) AS total
FROM data;
```

**Rows returned:** 1

| min_val | max_val | avg_val | total |
| --- | --- | --- | --- |
| 0 | 1 | 0.07 | 7943 |

---

## 9. Total PatientId by Gender

**Status:** OK

```sql
SELECT Gender, SUM(PatientId) AS total_PatientId
FROM data
GROUP BY Gender
ORDER BY total_PatientId DESC;
```

**Rows returned:** 2

| Gender | total_PatientId |
| --- | --- |
| F | 1.0489614877018673e+19 |
| M | 5.812704883154054e+18 |

---

## 10. Average PatientId by Gender

**Status:** OK

```sql
SELECT Gender, ROUND(AVG(PatientId), 2) AS avg_PatientId
FROM data
GROUP BY Gender
ORDER BY avg_PatientId DESC;
```

**Rows returned:** 2

| Gender | avg_PatientId |
| --- | --- |
| M | 150249564017733.47 |
| F | 146013570114402.47 |

---

## 11. Total AppointmentID by Gender

**Status:** OK

```sql
SELECT Gender, SUM(AppointmentID) AS total_AppointmentID
FROM data
GROUP BY Gender
ORDER BY total_AppointmentID DESC;
```

**Rows returned:** 2

| Gender | total_AppointmentID |
| --- | --- |
| F | 407644400697 |
| M | 219630048680 |

---

## 12. Distribution of Gender

**Status:** OK

```sql
SELECT Gender, COUNT(*) AS row_count
FROM data
GROUP BY Gender
ORDER BY row_count DESC;
```

**Rows returned:** 2

| Gender | row_count |
| --- | --- |
| F | 71840 |
| M | 38687 |

---

## 13. Distribution of AppointmentDay

**Status:** OK

```sql
SELECT AppointmentDay, COUNT(*) AS row_count
FROM data
GROUP BY AppointmentDay
ORDER BY row_count DESC;
```

**Rows returned:** 27

| AppointmentDay | row_count |
| --- | --- |
| 2016-06-06T00:00:00Z | 4692 |
| 2016-05-16T00:00:00Z | 4613 |
| 2016-05-09T00:00:00Z | 4520 |
| 2016-05-30T00:00:00Z | 4514 |
| 2016-06-08T00:00:00Z | 4479 |
| 2016-05-11T00:00:00Z | 4474 |
| 2016-06-01T00:00:00Z | 4464 |
| 2016-06-07T00:00:00Z | 4416 |
| 2016-05-12T00:00:00Z | 4394 |
| 2016-05-02T00:00:00Z | 4376 |
| 2016-05-18T00:00:00Z | 4373 |
| 2016-05-17T00:00:00Z | 4372 |
| 2016-06-02T00:00:00Z | 4310 |
| 2016-05-10T00:00:00Z | 4308 |
| 2016-05-31T00:00:00Z | 4279 |
| 2016-05-05T00:00:00Z | 4273 |
| 2016-05-19T00:00:00Z | 4270 |
| 2016-05-03T00:00:00Z | 4256 |
| 2016-05-04T00:00:00Z | 4168 |
| 2016-06-03T00:00:00Z | 4090 |

*…7 more rows not shown*

---

## 14. Distribution of No-show

**Status:** ERROR

```sql
SELECT No-show, COUNT(*) AS row_count
FROM data
GROUP BY No-show
ORDER BY row_count DESC;
```

**Error:** `no such column: No`

---

## 15. Top 10 Gender by PatientId

**Status:** OK

```sql
SELECT Gender, SUM(PatientId) AS total_PatientId
FROM data
GROUP BY Gender
ORDER BY total_PatientId DESC
LIMIT 10;
```

**Rows returned:** 2

| Gender | total_PatientId |
| --- | --- |
| F | 1.0489614877018673e+19 |
| M | 5.812704883154054e+18 |

---

## 16. Bottom 10 Gender by PatientId

**Status:** OK

```sql
SELECT Gender, SUM(PatientId) AS total_PatientId
FROM data
GROUP BY Gender
ORDER BY total_PatientId ASC
LIMIT 10;
```

**Rows returned:** 2

| Gender | total_PatientId |
| --- | --- |
| M | 5.812704883154054e+18 |
| F | 1.0489614877018673e+19 |

---

## 17. Top 10 AppointmentDay by PatientId

**Status:** OK

```sql
SELECT AppointmentDay, SUM(PatientId) AS total_PatientId
FROM data
GROUP BY AppointmentDay
ORDER BY total_PatientId DESC
LIMIT 10;
```

**Rows returned:** 10

| AppointmentDay | total_PatientId |
| --- | --- |
| 2016-06-06T00:00:00Z | 7.107293509750629e+17 |
| 2016-05-16T00:00:00Z | 7.061621546159485e+17 |
| 2016-05-09T00:00:00Z | 6.65720181853728e+17 |
| 2016-06-08T00:00:00Z | 6.63666086826516e+17 |
| 2016-05-30T00:00:00Z | 6.619145168620172e+17 |
| 2016-06-01T00:00:00Z | 6.585851729358166e+17 |
| 2016-05-17T00:00:00Z | 6.547708904932524e+17 |
| 2016-05-18T00:00:00Z | 6.468900114449965e+17 |
| 2016-05-11T00:00:00Z | 6.468128273114216e+17 |
| 2016-06-07T00:00:00Z | 6.460275099605478e+17 |

---

## 18. PatientId by Gender and AppointmentDay

**Status:** OK

```sql
SELECT Gender, AppointmentDay, SUM(PatientId) AS total_PatientId
FROM data
GROUP BY Gender, AppointmentDay
ORDER BY total_PatientId DESC;
```

**Rows returned:** 54

| Gender | AppointmentDay | total_PatientId |
| --- | --- | --- |
| F | 2016-06-06T00:00:00Z | 4.689961862397386e+17 |
| F | 2016-06-07T00:00:00Z | 4.446413656838629e+17 |
| F | 2016-05-16T00:00:00Z | 4.379365812733394e+17 |
| F | 2016-05-09T00:00:00Z | 4.3283704339695405e+17 |
| F | 2016-05-30T00:00:00Z | 4.319143003611394e+17 |
| F | 2016-06-08T00:00:00Z | 4.30510830767661e+17 |
| F | 2016-05-18T00:00:00Z | 4.287612937821349e+17 |
| F | 2016-05-17T00:00:00Z | 4.2136027096515603e+17 |
| F | 2016-05-31T00:00:00Z | 4.201052371580796e+17 |
| F | 2016-05-10T00:00:00Z | 4.1906461252241235e+17 |
| F | 2016-06-01T00:00:00Z | 4.175149603704715e+17 |
| F | 2016-05-02T00:00:00Z | 4.171169193961334e+17 |
| F | 2016-05-11T00:00:00Z | 4.0791650542555616e+17 |
| F | 2016-05-03T00:00:00Z | 4.013178239656257e+17 |
| F | 2016-06-02T00:00:00Z | 3.9942756187667757e+17 |
| F | 2016-05-05T00:00:00Z | 3.942479036584985e+17 |
| F | 2016-05-19T00:00:00Z | 3.932875609948182e+17 |
| F | 2016-05-12T00:00:00Z | 3.91394937572044e+17 |
| F | 2016-05-24T00:00:00Z | 3.913774392300557e+17 |
| F | 2016-05-13T00:00:00Z | 3.803295442015638e+17 |

*…34 more rows not shown*

---

## 19. Performance Breakdown by Gender

**Status:** OK

```sql
SELECT
    Gender,
    COUNT(*) AS transaction_count,
    SUM(PatientId) AS total_PatientId,
    SUM(AppointmentID) AS total_AppointmentID,
    SUM(Age) AS total_Age,
    SUM(Scholarship) AS total_Scholarship,
    SUM(Hipertension) AS total_Hipertension,
    SUM(Diabetes) AS total_Diabetes
FROM data
GROUP BY Gender
ORDER BY total_PatientId DESC;
```

**Rows returned:** 2

| Gender | transaction_count | total_PatientId | total_AppointmentID | total_Age | total_Scholarship | total_Hipertension | total_Diabetes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F | 71840 | 1.0489614877018673e+19 | 407644400697 | 2794144 | 8853 | 15339 | 5606 |
| M | 38687 | 5.812704883154054e+18 | 219630048680 | 1305178 | 2008 | 6462 | 2337 |

---

## 20. Performance Breakdown by AppointmentDay

**Status:** OK

```sql
SELECT
    AppointmentDay,
    COUNT(*) AS transaction_count,
    SUM(PatientId) AS total_PatientId,
    SUM(AppointmentID) AS total_AppointmentID,
    SUM(Age) AS total_Age,
    SUM(Scholarship) AS total_Scholarship,
    SUM(Hipertension) AS total_Hipertension,
    SUM(Diabetes) AS total_Diabetes
FROM data
GROUP BY AppointmentDay
ORDER BY total_PatientId DESC;
```

**Rows returned:** 27

| AppointmentDay | transaction_count | total_PatientId | total_AppointmentID | total_Age | total_Scholarship | total_Hipertension | total_Diabetes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2016-06-06T00:00:00Z | 4692 | 7.107293509750629e+17 | 26922870225 | 172478 | 458 | 849 | 309 |
| 2016-05-16T00:00:00Z | 4613 | 7.061621546159485e+17 | 26125671383 | 167682 | 461 | 870 | 313 |
| 2016-05-09T00:00:00Z | 4520 | 6.65720181853728e+17 | 25490244728 | 167632 | 403 | 896 | 312 |
| 2016-06-08T00:00:00Z | 4479 | 6.63666086826516e+17 | 25748963124 | 166911 | 458 | 900 | 317 |
| 2016-05-30T00:00:00Z | 4514 | 6.619145168620172e+17 | 25726843927 | 167559 | 482 | 868 | 315 |
| 2016-06-01T00:00:00Z | 4464 | 6.585851729358166e+17 | 25533932037 | 170123 | 433 | 880 | 330 |
| 2016-05-17T00:00:00Z | 4372 | 6.547708904932524e+17 | 24798385463 | 161495 | 401 | 812 | 291 |
| 2016-05-18T00:00:00Z | 4373 | 6.468900114449965e+17 | 24812864108 | 159536 | 427 | 838 | 317 |
| 2016-05-11T00:00:00Z | 4474 | 6.468128273114216e+17 | 25269760048 | 164058 | 423 | 840 | 311 |
| 2016-06-07T00:00:00Z | 4416 | 6.460275099605478e+17 | 25371834575 | 162629 | 411 | 875 | 340 |
| 2016-05-10T00:00:00Z | 4308 | 6.403347623085932e+17 | 24324249015 | 158843 | 436 | 855 | 340 |
| 2016-05-31T00:00:00Z | 4279 | 6.390073683098787e+17 | 24422394356 | 161793 | 434 | 887 | 300 |
| 2016-05-12T00:00:00Z | 4394 | 6.378221432404353e+17 | 24842042934 | 161067 | 432 | 866 | 306 |
| 2016-05-02T00:00:00Z | 4376 | 6.361482195341268e+17 | 24555484960 | 161149 | 416 | 907 | 322 |
| 2016-05-19T00:00:00Z | 4270 | 6.300627228750563e+17 | 24245996161 | 157928 | 381 | 832 | 272 |
| 2016-06-02T00:00:00Z | 4310 | 6.274775062425944e+17 | 24680269029 | 164647 | 398 | 897 | 321 |
| 2016-05-03T00:00:00Z | 4256 | 6.244184188086084e+17 | 23913201543 | 159051 | 468 | 889 | 315 |
| 2016-06-03T00:00:00Z | 4090 | 6.135990429157101e+17 | 23426852327 | 157375 | 403 | 874 | 343 |
| 2016-05-05T00:00:00Z | 4273 | 6.048848400776709e+17 | 24046880798 | 158640 | 447 | 873 | 304 |
| 2016-05-13T00:00:00Z | 3987 | 5.914162140897514e+17 | 22550835091 | 146413 | 414 | 812 | 311 |

*…7 more rows not shown*

---

## 21. Performance Breakdown by No-show

**Status:** ERROR

```sql
SELECT
    No-show,
    COUNT(*) AS transaction_count,
    SUM(PatientId) AS total_PatientId,
    SUM(AppointmentID) AS total_AppointmentID,
    SUM(Age) AS total_Age,
    SUM(Scholarship) AS total_Scholarship,
    SUM(Hipertension) AS total_Hipertension,
    SUM(Diabetes) AS total_Diabetes
FROM data
GROUP BY No-show
ORDER BY total_PatientId DESC;
```

**Error:** `no such column: No`

---

## 22. Gender × AppointmentDay Performance Matrix

**Status:** OK

```sql
SELECT
    Gender,
    AppointmentDay,
    COUNT(*) AS transaction_count,
    SUM(PatientId) AS total_PatientId,
    SUM(AppointmentID) AS total_AppointmentID,
    SUM(Age) AS total_Age,
    SUM(Scholarship) AS total_Scholarship
FROM data
GROUP BY Gender, AppointmentDay
ORDER BY total_PatientId DESC;
```

**Rows returned:** 54

| Gender | AppointmentDay | transaction_count | total_PatientId | total_AppointmentID | total_Age | total_Scholarship |
| --- | --- | --- | --- | --- | --- | --- |
| F | 2016-06-06T00:00:00Z | 3087 | 4.689961862397386e+17 | 17711210078 | 119853 | 355 |
| F | 2016-06-07T00:00:00Z | 2951 | 4.446413656838629e+17 | 16951524765 | 114751 | 330 |
| F | 2016-05-16T00:00:00Z | 2948 | 4.379365812733394e+17 | 16688131992 | 111995 | 375 |
| F | 2016-05-09T00:00:00Z | 2901 | 4.3283704339695405e+17 | 16358059478 | 112945 | 333 |
| F | 2016-05-30T00:00:00Z | 2922 | 4.319143003611394e+17 | 16648708668 | 113988 | 389 |
| F | 2016-06-08T00:00:00Z | 2967 | 4.30510830767661e+17 | 17053659579 | 116695 | 369 |
| F | 2016-05-18T00:00:00Z | 2841 | 4.287612937821349e+17 | 16119247938 | 107879 | 348 |
| F | 2016-05-17T00:00:00Z | 2919 | 4.2136027096515603e+17 | 16553795149 | 113966 | 330 |
| F | 2016-05-31T00:00:00Z | 2798 | 4.201052371580796e+17 | 15964597720 | 109735 | 366 |
| F | 2016-05-10T00:00:00Z | 2803 | 4.1906461252241235e+17 | 15822825074 | 108866 | 361 |
| F | 2016-06-01T00:00:00Z | 2905 | 4.175149603704715e+17 | 16613639349 | 115006 | 353 |
| F | 2016-05-02T00:00:00Z | 2819 | 4.171169193961334e+17 | 15815654548 | 108936 | 347 |
| F | 2016-05-11T00:00:00Z | 2905 | 4.0791650542555616e+17 | 16404103774 | 112960 | 342 |
| F | 2016-05-03T00:00:00Z | 2766 | 4.013178239656257e+17 | 15536760556 | 108206 | 384 |
| F | 2016-06-02T00:00:00Z | 2746 | 3.9942756187667757e+17 | 15721610971 | 109376 | 322 |
| F | 2016-05-05T00:00:00Z | 2808 | 3.942479036584985e+17 | 15799624973 | 109951 | 366 |
| F | 2016-05-19T00:00:00Z | 2743 | 3.932875609948182e+17 | 15569493484 | 107321 | 316 |
| F | 2016-05-12T00:00:00Z | 2821 | 3.91394937572044e+17 | 15949387153 | 109345 | 351 |
| F | 2016-05-24T00:00:00Z | 2637 | 3.913774392300557e+17 | 15025118793 | 104096 | 328 |
| F | 2016-05-13T00:00:00Z | 2574 | 3.803295442015638e+17 | 14553279372 | 99615 | 324 |

*…34 more rows not shown*

---

## 23. Filter by Gender

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE Gender = :Gender;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 24. Performance Summary for a Specific Gender

**Status:** SKIPPED

```sql
SELECT
    Gender,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId,
    ROUND(SUM(AppointmentID), 2) AS total_AppointmentID
FROM data
WHERE Gender = :Gender
GROUP BY Gender;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 25. AppointmentDay Breakdown for Gender = :Gender

**Status:** SKIPPED

```sql
SELECT
    AppointmentDay,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE Gender = :Gender
GROUP BY AppointmentDay
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 26. Neighbourhood Breakdown for Gender = :Gender

**Status:** SKIPPED

```sql
SELECT
    Neighbourhood,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE Gender = :Gender
GROUP BY Neighbourhood
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 27. Filter by AppointmentDay

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE AppointmentDay = :AppointmentDay;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 28. Performance Summary for a Specific AppointmentDay

**Status:** SKIPPED

```sql
SELECT
    AppointmentDay,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId,
    ROUND(SUM(AppointmentID), 2) AS total_AppointmentID
FROM data
WHERE AppointmentDay = :AppointmentDay
GROUP BY AppointmentDay;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 29. Gender Breakdown for AppointmentDay = :AppointmentDay

**Status:** SKIPPED

```sql
SELECT
    Gender,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE AppointmentDay = :AppointmentDay
GROUP BY Gender
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 30. Neighbourhood Breakdown for AppointmentDay = :AppointmentDay

**Status:** SKIPPED

```sql
SELECT
    Neighbourhood,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE AppointmentDay = :AppointmentDay
GROUP BY Neighbourhood
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 31. Filter by Neighbourhood

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE Neighbourhood = :Neighbourhood;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 32. Performance Summary for a Specific Neighbourhood

**Status:** SKIPPED

```sql
SELECT
    Neighbourhood,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId,
    ROUND(SUM(AppointmentID), 2) AS total_AppointmentID
FROM data
WHERE Neighbourhood = :Neighbourhood
GROUP BY Neighbourhood;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 33. Gender Breakdown for Neighbourhood = :Neighbourhood

**Status:** SKIPPED

```sql
SELECT
    Gender,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE Neighbourhood = :Neighbourhood
GROUP BY Gender
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 34. AppointmentDay Breakdown for Neighbourhood = :Neighbourhood

**Status:** SKIPPED

```sql
SELECT
    AppointmentDay,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE Neighbourhood = :Neighbourhood
GROUP BY AppointmentDay
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 35. Filter by No-show

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE No-show = :No-show;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 36. Performance Summary for a Specific No-show

**Status:** SKIPPED

```sql
SELECT
    No-show,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId,
    ROUND(SUM(AppointmentID), 2) AS total_AppointmentID
FROM data
WHERE No-show = :No-show
GROUP BY No-show;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 37. Gender Breakdown for No-show = :No-show

**Status:** SKIPPED

```sql
SELECT
    Gender,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE No-show = :No-show
GROUP BY Gender
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 38. AppointmentDay Breakdown for No-show = :No-show

**Status:** SKIPPED

```sql
SELECT
    AppointmentDay,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
WHERE No-show = :No-show
GROUP BY AppointmentDay
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 39. Rows Where PatientId Exceeds :min_value

**Status:** SKIPPED

```sql
SELECT *
FROM data
WHERE PatientId > :min_value
ORDER BY PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 40. Gender with Total PatientId Above :threshold

**Status:** SKIPPED

```sql
SELECT
    Gender,
    COUNT(*) AS transaction_count,
    ROUND(SUM(PatientId), 2) AS total_PatientId
FROM data
GROUP BY Gender
HAVING SUM(PatientId) > :threshold
ORDER BY total_PatientId DESC;
```

**Skipped:** Query requires runtime arguments (:param)

---

## 41. Missing Values per Column

**Status:** OK

```sql
SELECT 'PatientId' AS column_name, COUNT(*) AS null_count FROM data WHERE PatientId IS NULL
UNION ALL
SELECT 'AppointmentID' AS column_name, COUNT(*) AS null_count FROM data WHERE AppointmentID IS NULL
UNION ALL
SELECT 'Gender' AS column_name, COUNT(*) AS null_count FROM data WHERE Gender IS NULL
UNION ALL
SELECT 'ScheduledDay' AS column_name, COUNT(*) AS null_count FROM data WHERE ScheduledDay IS NULL
UNION ALL
SELECT 'AppointmentDay' AS column_name, COUNT(*) AS null_count FROM data WHERE AppointmentDay IS NULL
UNION ALL
SELECT 'Age' AS column_name, COUNT(*) AS null_count FROM data WHERE Age IS NULL
UNION ALL
SELECT 'Neighbourhood' AS column_name, COUNT(*) AS null_count FROM data WHERE Neighbourhood IS NULL
UNION ALL
SELECT 'Scholarship' AS column_name, COUNT(*) AS null_count FROM data WHERE Scholarship IS NULL
UNION ALL
SELECT 'Hipertension' AS column_name, COUNT(*) AS null_count FROM data WHERE Hipertension IS NULL
UNION ALL
SELECT 'Diabetes' AS column_name, COUNT(*) AS null_count FROM data WHERE Diabetes IS NULL
UNION ALL
SELECT 'Alcoholism' AS column_name, COUNT(*) AS null_count FROM data WHERE Alcoholism IS NULL
UNION ALL
SELECT 'Handcap' AS column_name, COUNT(*) AS null_count FROM data WHERE Handcap IS NULL
ORDER BY null_count DESC;
```

**Rows returned:** 12

| column_name | null_count |
| --- | --- |
| PatientId | 0 |
| AppointmentID | 0 |
| Gender | 0 |
| ScheduledDay | 0 |
| AppointmentDay | 0 |
| Age | 0 |
| Neighbourhood | 0 |
| Scholarship | 0 |
| Hipertension | 0 |
| Diabetes | 0 |
| Alcoholism | 0 |
| Handcap | 0 |

---

## 42. Negative PatientId Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE PatientId < 0
ORDER BY PatientId;
```

**Rows returned:** 0

*(no rows returned)*

---

## 43. Negative AppointmentID Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE AppointmentID < 0
ORDER BY AppointmentID;
```

**Rows returned:** 0

*(no rows returned)*

---

## 44. Negative Age Values

**Status:** OK

```sql
SELECT *
FROM data
WHERE Age < 0
ORDER BY Age;
```

**Rows returned:** 1

| PatientId | AppointmentID | Gender | ScheduledDay | AppointmentDay | Age | Neighbourhood | Scholarship | Hipertension | Diabetes | Alcoholism | Handcap | SMS_received | No-show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 465943158731293.0 | 5775010 | F | 2016-06-06T08:58:13Z | 2016-06-06T00:00:00Z | -1 | ROMÃO | 0 | 0 | 0 | 0 | 0 | 0 | No |

---
