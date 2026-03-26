# Dirty Row Report

- **Total rows in dataset:** 50
- **Dirty rows identified:** 3
- **Clean rows:** 47

## Criteria Used

A row is flagged as **dirty** if it satisfies one or more of the following conditions:

| # | Criterion | Description |
|---|-----------|-------------|
| 1 | **Missing value** | One or more cells are null / NaN |
| 2 | **Exact duplicate** | Row is an identical copy of an earlier row |
| 3 | **Numeric outlier** | A numeric value falls outside +/- 3 standard deviations from the column mean |
| 4 | **Negative in non-negative column** | A numeric value is negative in a column whose name implies non-negative values (price, quantity, total, etc.) |

## Summary by Criterion

- **Missing values:** 2 row(s)
- **Numeric outliers (+/-3 std dev):** 1 row(s)
- **Negative in non-negative column:** 1 row(s)

## Row-by-Row Detail

### Row 9
- Missing value(s) in column(s): customer_id, customer_name

### Row 10
- Outlier in 'total_price': 8000 (mean=1741, +/-3 std dev threshold=[-4398, 7879])

### Row 34
- Missing value(s) in column(s): total_price
- Negative value in 'quantity': -1 (expected ≥ 0)

