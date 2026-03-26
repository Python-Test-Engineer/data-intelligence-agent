# Insights: Overview Numeric Distributions

![overview_numeric_distributions.png](../images/overview_numeric_distributions.png)

## Data Insight
- The numeric variables show distinct distribution patterns. Unit price exhibits high variability (CV=92%) with mean 403.49 and substantial right skew likely present. Total price mirrors this pattern with mean 2695.93 and CV of 95%, indicating a few high-value transactions driving the distribution. Quantity shows tighter clustering around mean 6.65 with lower relative variability (CV=29%).

## Analysis Insight
- The distributions suggest most transactions involve moderate unit prices and quantities, with outlier high-value orders inflating totals. Unit price and total price distributions likely exhibit positive skew given the ratio of standard deviation to mean exceeding 0.9. Quantity's lower dispersion indicates more consistent order sizes across transactions compared to monetary variables.

## Caveat
- Inferences are limited by small sample size (n=20) and lack of visible chart details; distributional shapes cannot be confirmed without histogram or boxplot visualization. Summary statistics alone cannot capture potential multimodality or specific outlier values driving the high variance in monetary fields.
