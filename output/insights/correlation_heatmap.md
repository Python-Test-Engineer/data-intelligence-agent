# Insights: Correlation Heatmap

![correlation_heatmap.png](../images/correlation_heatmap.png)

## Data Insight
- The correlation heatmap likely shows strong positive correlations among cost, revenue, and profit variables. unit_cost and unit_price probably exhibit moderate-to-strong positive correlation, as do quantity with total_cost and total_revenue. profit likely correlates strongly with total_revenue and total_cost. margin_pct may show weaker or negative correlations with unit_cost and quantity.

## Analysis Insight
- Sales value metrics (total_cost, total_revenue, profit) cluster together with high intercorrelations, as expected from their definitional relationships. The relationship between pricing variables (unit_cost, unit_price) and volume variables (quantity) may reveal whether the business uses cost-plus pricing or considers demand elasticity. Store-level or customer-level variables likely show weaker correlations with financial metrics.

## Caveat
- Correlation heatmaps only capture linear relationships and may obscure non-linear associations. Confounding variables (e.g., product category, seasonal effects) not visible in the heatmap may drive observed correlations. The 100-row sample may lack statistical power for detecting modest correlations, and categorical variables were excluded from correlation analysis.
