# Insights: Overview Numeric Distributions

![overview_numeric_distributions.png](../images/overview_numeric_distributions.png)

## Data Insight
- The numeric distributions show right-skewed patterns. Unit price (mean=305.99, std=328.79) spans a wide range with high variability. Quantity (mean=5.60, std=2.48) clusters more tightly around lower values. Total price (mean=1740.55, std=2046.17) exhibits the highest dispersion, driven by the multiplicative effect of price times quantity.

## Analysis Insight
- Unit price and total price distributions likely contain outliers or premium products driving the high standard deviations. The quantity distribution appears more normally distributed with moderate spread. The ratio of std to mean exceeds 1.0 for both price variables, indicating non-normal, skewed distributions typical of sales data.

## Caveat
- Without seeing the actual chart, these insights are inferred from summary statistics alone. The analysis cannot confirm distribution shapes, detect specific outliers, or account for potential data entry errors or temporal patterns in the 50-order sample.
