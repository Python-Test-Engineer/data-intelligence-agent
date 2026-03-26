# Insights: Correlation Heatmap

![correlation_heatmap.png](../images/correlation_heatmap.png)

## Data Insight
- A correlation heatmap of 50 transactions shows strong positive correlation between total_price and unit_price (r≈0.85) and between total_price and quantity (r≈0.75). ID variables (order_id, customer_id, product_id, store_id) exhibit minimal correlation with numeric metrics. Payment_method and city, when encoded, display weak associations with sales values.

## Analysis Insight
- The total_price correlates strongly with both unit_price and quantity as expected from the formula total_price = unit_price × quantity. Low correlation among ID variables indicates randomness in order/customer/product assignment. Weak payment_method correlations suggest no strong payment preference effect on purchase amounts.

## Caveat
- With only 50 rows, correlation estimates have high uncertainty; small sample limits detection of modest effects. Encoded categorical variables may introduce artificial correlations. Temporal patterns in date cannot be assessed via simple correlation. Confounding between product type and price tier may inflate observed relationships.
