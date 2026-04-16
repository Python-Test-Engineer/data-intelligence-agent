# Final Data Insights

- Generated: 2026-04-16 11:26 UTC
- Model setting: google/gemini-2.5-flash-lite
- LLM-enabled: yes
- Individual insight files: 10

## Dataset Context
- Rows: 3
- Columns: 7
- Numeric columns: 3
- quantity: mean=7.67, std=2.52
- unit_price: mean=153.32, std=172.14
- total_price: mean=1429.92, std=1809.31

## Consolidated Chart Insights

## Generation Notes
- LLM generation failed for one or more charts; heuristic fallback was used.
- category_category.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- category_city.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- category_order_id.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- category_product.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- correlation_heatmap.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- distribution_quantity.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- distribution_total_price.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- distribution_unit_price.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- overview_numeric_distributions.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}
- overview_scatter_unit_price_vs_total_price.png: Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}

### Category Category

# Insights: Category Category

![category_category.png](../images/category_category.png)

## Data Insight
- 'Accessories' is the most frequent value in 'category'. Imbalanced categories may skew aggregates and require stratified analysis.

## Analysis Insight
- Rare categories can be grouped into an 'Other' bucket to reduce noise and improve model generalisation.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Category City

# Insights: Category City

![category_city.png](../images/category_city.png)

## Data Insight
- 'Accessories' is the most frequent value in 'category'. Imbalanced categories may skew aggregates and require stratified analysis.

## Analysis Insight
- Rare categories can be grouped into an 'Other' bucket to reduce noise and improve model generalisation.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Category Order Id

# Insights: Category Order Id

![category_order_id.png](../images/category_order_id.png)

## Data Insight
- 'ORD001' is the most frequent value in 'order_id'. Imbalanced categories may skew aggregates and require stratified analysis.

## Analysis Insight
- Rare categories can be grouped into an 'Other' bucket to reduce noise and improve model generalisation.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Category Product

# Insights: Category Product

![category_product.png](../images/category_product.png)

## Data Insight
- 'Monitor' is the most frequent value in 'product'. Imbalanced categories may skew aggregates and require stratified analysis.

## Analysis Insight
- Rare categories can be grouped into an 'Other' bucket to reduce noise and improve model generalisation.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Correlation Heatmap

# Insights: Correlation Heatmap

![correlation_heatmap.png](../images/correlation_heatmap.png)

## Data Insight
- The strongest correlation is between 'unit_price' and 'total_price' (r ≈ 1.00), suggesting these columns move together and may be related.

## Analysis Insight
- Use this map to reduce collinearity in downstream models and prioritise orthogonal feature subsets.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Distribution Quantity

# Insights: Distribution Quantity

![distribution_quantity.png](../images/distribution_quantity.png)

## Data Insight
- The distribution of 'quantity' reveals the spread and shape of values. Skewed distributions or outliers may warrant transformation before modelling.

## Analysis Insight
- Highly skewed distributions may benefit from log or Box-Cox transformation before statistical modelling.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Distribution Total Price

# Insights: Distribution Total Price

![distribution_total_price.png](../images/distribution_total_price.png)

## Data Insight
- The distribution of 'total price' reveals the spread and shape of values. Skewed distributions or outliers may warrant transformation before modelling.

## Analysis Insight
- Highly skewed distributions may benefit from log or Box-Cox transformation before statistical modelling.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Distribution Unit Price

# Insights: Distribution Unit Price

![distribution_unit_price.png](../images/distribution_unit_price.png)

## Data Insight
- The distribution of 'unit price' reveals the spread and shape of values. Skewed distributions or outliers may warrant transformation before modelling.

## Analysis Insight
- Highly skewed distributions may benefit from log or Box-Cox transformation before statistical modelling.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Overview Numeric Distributions

# Insights: Overview Numeric Distributions

![overview_numeric_distributions.png](../images/overview_numeric_distributions.png)

## Data Insight
- The dataset contains 3 numeric column(s). This chart compares their spread, helping spot outliers and scale differences.

## Analysis Insight
- Consider normalising or scaling columns with very different ranges before applying distance-based algorithms.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

### Overview Scatter Unit Price Vs Total Price

# Insights: Overview Scatter Unit Price Vs Total Price

![overview_scatter_unit_price_vs_total_price.png](../images/overview_scatter_unit_price_vs_total_price.png)

## Data Insight
- This scatter plot reveals the relationship between two numeric columns. Clusters or linear trends can motivate correlation and regression analyses.

## Analysis Insight
- The bivariate structure can motivate interaction terms and subgroup analyses in regression models.

## Caveat
- Insights are exploratory and non-causal. Missing cells in source data: 0. Sample size, data quality, and unmeasured variables may affect conclusions.

