# CSV Dataset Report

## Dataset Snapshot
- Rows: 20
- Columns: 7
- Numeric columns: 3
- Categorical columns: 3
- Date/time columns: date
- Missing cells: 0

## Numeric Summary
- **unit_price**: mean=403.49, std=370.34, min=29.99, max=999.99, median=349.99
- **quantity**: mean=6.65, std=1.95, min=3.00, max=10.00, median=7.00
- **total_price**: mean=2695.93, std=2567.29, min=89.97, max=7999.92, median=1549.93

## Top Category Distributions
### order_id (top 5 of 20 unique values)
- ORD0001: 1 (5.0%)
- ORD0002: 1 (5.0%)
- ORD0003: 1 (5.0%)
- ORD0004: 1 (5.0%)
- ORD0005: 1 (5.0%)
### product_name (top 5 of 5 unique values)
- Monitor: 6 (30.0%)
- Headphones: 5 (25.0%)
- Laptop: 5 (25.0%)
- Mouse: 2 (10.0%)
- Keyboard: 2 (10.0%)
### city (top 3 of 3 unique values)
- Los Angeles: 8 (40.0%)
- New York: 7 (35.0%)
- Chicago: 5 (25.0%)

## Top Correlations
- unit_price vs total_price: r = 0.945
- quantity vs total_price: r = 0.260
- unit_price vs quantity: r = 0.019

## Chart Index
- overview_numeric_distributions.png (overview)
- correlation_heatmap.png (correlation)
- distribution_unit_price.png (distribution)
- distribution_quantity.png (distribution)
- distribution_total_price.png (distribution)
- category_order_id.png (category)
- category_product_name.png (category)
- category_city.png (category)
- time_series_unit_price.png (time)
- time_series_quantity.png (time)
- time_series_total_price.png (time)
- overview_scatter_unit_price_vs_total_price.png (overview)

## Caveats
- This report is exploratory. Observed patterns should be validated before drawing conclusions.
- Missingness and data quality may influence results.
