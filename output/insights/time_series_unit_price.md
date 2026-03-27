# Insights: Time Series Unit Price

![time_series_unit_price.png](../images/time_series_unit_price.png)

## Data Insight
- The time series displays unit price fluctuations across the 100-order period with a mean of 376.69 and high variability (std=370.50). Unit prices range widely from low values to peaks exceeding the mean significantly. Temporal clustering of high-value orders appears at specific points, with periods of lower, more stable pricing between spikes.

## Analysis Insight
- The substantial standard deviation relative to the mean indicates unit price volatility likely driven by product mix variation or pricing strategy changes. Given unit_cost mean of 219.84, the average markup is approximately 156.85 per unit. The quantity mean of 6.12 suggests bulk purchases may correlate with price variations.

## Caveat
- Without product-level identifiers or timestamp granularity, trends may reflect confounding product composition changes rather than true price dynamics. The 100-row sample limits trend generalizability, and without store or time period metadata, seasonal effects or external factors cannot be assessed.
