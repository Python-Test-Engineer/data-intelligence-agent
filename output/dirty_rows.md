# Dirty Row Report

- **Total rows in dataset:** 100
- **Dirty rows identified:** 4
- **Clean rows:** 96

## Criteria Used

A row is flagged as **dirty** if it satisfies one or more of the following conditions:

| # | Criterion | Description |
|---|-----------|-------------|
| 1 | **Missing value** | One or more cells are null / NaN |
| 2 | **Exact duplicate** | Row is an identical copy of an earlier row |
| 3 | **Numeric outlier** | A numeric value falls outside +/- 3 standard deviations from the column mean |
| 4 | **Negative in non-negative column** | A numeric value is negative in a column whose name implies non-negative values (price, quantity, total, etc.) |

## Summary by Criterion

- **Missing values:** 3 row(s)
- **Exact duplicates:** 1 row(s)
- **Negative in non-negative column:** 1 row(s)

## Row-by-Row Detail

### Row 38
- Exact duplicate of a previous row

### Row 40
- Missing value(s) in column(s): unit_cost, total_cost, profit, margin_pct

### Row 55
- Missing value(s) in column(s): total_cost, total_revenue, profit, margin_pct
- Negative value in 'quantity': -1 (expected ≥ 0)

### Row 97
- Missing value(s) in column(s): customer_id, customer_name

