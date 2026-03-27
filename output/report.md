# CSV Dataset Report

## Dataset Snapshot
- Rows: 100
- Columns: 17
- Numeric columns: 7
- Categorical columns: 9
- Date/time columns: date
- Missing cells: 10

## Numeric Summary
- **unit_cost**: mean=219.84, std=252.72, min=8.50, max=650.00, median=180.00
- **unit_price**: mean=376.69, std=370.50, min=29.99, max=999.99, median=349.99
- **quantity**: mean=6.12, std=2.88, min=-1.00, max=10.00, median=7.00
- **total_cost**: mean=1341.73, std=1753.29, min=17.00, max=6500.00, median=440.00
- **total_revenue**: mean=2308.02, std=2624.08, min=59.98, max=9999.90, median=1049.93
- **profit**: mean=964.84, std=902.45, min=42.98, max=3499.90, median=617.43
- **margin_pct**: mean=54.07, std=13.47, min=35.00, max=71.70, median=48.60

## Top Category Distributions
### customer_id (top 5 of 10 unique values)
- C02: 16 (16.0%)
- C04: 14 (14.0%)
- C09: 12 (12.0%)
- C05: 12 (12.0%)
- C07: 11 (11.0%)
### customer_name (top 5 of 10 unique values)
- Bob Smith: 16 (16.0%)
- David Brown: 14 (14.0%)
- Isabella Taylor: 12 (12.0%)
- Emma Davis: 12 (12.0%)
- Grace Wilson: 11 (11.0%)
### product_id (top 5 of 5 unique values)
- P004: 27 (27.0%)
- P001: 24 (24.0%)
- P003: 19 (19.0%)
- P005: 15 (15.0%)
- P002: 15 (15.0%)
### product_name (top 5 of 6 unique values)
- Monitor: 27 (27.0%)
- Laptop: 24 (24.0%)
- Keyboard: 19 (19.0%)
- Headphones: 15 (15.0%)
- Mouse: 14 (14.0%)
### store_id (top 3 of 3 unique values)
- S3: 37 (37.0%)
- S2: 34 (34.0%)
- S1: 29 (29.0%)

## Top Correlations
- unit_cost vs unit_price: r = 0.998
- total_cost vs total_revenue: r = 0.996
- total_revenue vs profit: r = 0.987
- total_cost vs profit: r = 0.970
- unit_price vs margin_pct: r = -0.950

## Chart Index
- overview_numeric_distributions.png (overview)
- correlation_heatmap.png (correlation)
- distribution_unit_cost.png (distribution)
- distribution_unit_price.png (distribution)
- distribution_quantity.png (distribution)
- distribution_total_cost.png (distribution)
- distribution_total_revenue.png (distribution)
- distribution_profit.png (distribution)
- category_customer_id.png (category)
- category_customer_name.png (category)
- category_product_id.png (category)
- category_product_name.png (category)
- category_store_id.png (category)
- category_store_name.png (category)
- category_city.png (category)
- category_payment_method.png (category)
- time_series_unit_cost.png (time)
- time_series_unit_price.png (time)
- time_series_quantity.png (time)
- overview_scatter_unit_cost_vs_unit_price.png (overview)

## Caveats
- This report is exploratory. Observed patterns should be validated before drawing conclusions.
- Missingness and data quality may influence results.
