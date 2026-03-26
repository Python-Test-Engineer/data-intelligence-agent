# Insights: Overview Scatter Unit Price Vs Total Price

![overview_scatter_unit_price_vs_total_price.png](../images/overview_scatter_unit_price_vs_total_price.png)

## Data Insight
- The scatter plot displays 20 data points plotting unit_price against total_price. Unit prices range from near 0 to approximately 1,200, while total prices span from near 0 to around 9,000. A clear positive linear trend is visible, with points clustered in the lower-left region and a few outliers extending toward higher values in both dimensions.

## Analysis Insight
- The positive linear relationship aligns with the mathematical relationship total_price = unit_price × quantity. The dispersion around the trend reflects variation in quantity ordered (mean=6.65, std=1.95). Higher unit price transactions tend to show greater total price variance, suggesting inconsistent order quantities across price segments.

## Caveat
- This analysis is limited to 20 observations, restricting statistical power and generalizability. The scatter reveals correlation but not causation; quantity serves as a confounding variable. City and product effects are not visible, and temporal patterns cannot be assessed from this static view.
