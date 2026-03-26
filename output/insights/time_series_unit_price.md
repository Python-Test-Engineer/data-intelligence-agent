# Insights: Time Series Unit Price

![time_series_unit_price.png](../images/time_series_unit_price.png)

## Data Insight
- Unit price exhibits high variability (mean 305.99, std 328.79), suggesting diverse product pricing or price fluctuations over the time series period. The ratio of total_price mean (1740.55) to unit_price mean indicates orders typically involve multiple units (approx 5.7 units on average, consistent with quantity mean of 5.60).

## Analysis Insight
- The time series likely captures temporal patterns in unit pricing across different products and stores. High standard deviation relative to mean suggests a wide price range or volatile pricing. Customer and store distributions across cities likely contribute to price variation.

## Caveat
- Analysis based on dataset metadata alone without visual chart access; actual trend direction, seasonality, or outliers cannot be confirmed. Summary statistics may be influenced by extreme values given the high standard deviation. Confounding factors (product type, store location, time period) not controlled.
