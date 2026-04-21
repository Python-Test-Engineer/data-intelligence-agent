# Dirty Row Report

- **Total rows in dataset:** 20
- **Dirty rows identified:** 0
- **Clean rows:** 20

## Criteria Used

A row is flagged as **dirty** if it satisfies one or more of the following conditions:

| # | Criterion | Description |
|---|-----------|-------------|
| 1 | **Missing value** | One or more cells are null / NaN |
| 2 | **Exact duplicate** | Row is an identical copy of an earlier row |
| 3 | **Numeric outlier** | A numeric value falls outside +/- 3 standard deviations from the column mean |
| 4 | **Negative in non-negative column** | A numeric value is negative in a column whose name implies non-negative values (price, quantity, total, etc.) |

## Result

No dirty rows were detected. The dataset appears clean.
