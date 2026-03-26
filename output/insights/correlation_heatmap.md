# Insights: Correlation Heatmap

![correlation_heatmap.png](../images/correlation_heatmap.png)

## Data Insight
- A correlation heatmap of numeric variables (unit_price, quantity, total_price) likely shows strong positive correlations between total_price and both unit_price (r > 0.7) and quantity, reflecting the mathematical relationship total_price = unit_price × quantity.

## Analysis Insight
- The presence of high correlation between total_price and its components indicates multicollinearity if used together in predictive modeling. Order_id should not be included as it represents an identifier, not a meaningful numeric variable.

## Caveat
- Without seeing the actual chart, correlations are inferred from data structure. The heatmap may include misleading correlations if order_id was treated as numeric. City (categorical) requires encoding to appear in correlation analysis.
