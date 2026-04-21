# Insights: Category Order Id

![category_order_id.png](../images/category_order_id.png)

## Data Insight
- 'ORD0001' is the most frequent value in 'order_id'. Imbalanced categories may skew aggregates and require stratified analysis.

## Analysis Insight
- Rare categories can be grouped into an 'Other' bucket to reduce noise and improve model generalisation.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.
