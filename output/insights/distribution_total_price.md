# Insights: Distribution Total Price

![distribution_total_price.png](../images/distribution_total_price.png)

## Data Insight
- Total price distribution shows high right-skew with mean=2695.93 and std=2567.29. Coefficient of variation near 0.95 indicates extreme spread, suggesting few high-value orders pulling the mean above the median.

## Analysis Insight
- The high standard deviation relative to mean implies heterogeneous purchasing patterns. Combined with quantity mean of 6.65 (low std=1.95), total price variation likely stems from unit price variability (mean=403.49, std=370.34) rather than order size differences.

## Caveat
- Small sample (n=20) limits distributional inference; cannot reliably assess skewness or identify outliers without raw values. City-level effects unexamined; summary stats alone cannot confirm distributional shape.
