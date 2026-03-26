# CSV Dataset Report

## Dataset Snapshot
- Rows: 50
- Columns: 13
- Numeric columns: 3
- Categorical columns: 9
- Date/time columns: date
- Missing cells: 3

## Numeric Summary
- **unit_price**: mean=305.99, std=328.79, min=29.99, max=999.99, median=149.99
- **quantity**: mean=5.60, std=2.48, min=-1.00, max=10.00, median=6.00
- **total_price**: mean=1740.55, std=2046.17, min=29.99, max=7999.92, median=899.94

## Top Category Distributions
### customer_id (top 5 of 10 unique values)
- C02: 10 (20.0%)
- C03: 8 (16.0%)
- C08: 7 (14.0%)
- C10: 4 (8.0%)
- C09: 4 (8.0%)
### customer_name (top 5 of 10 unique values)
- Bob Smith: 10 (20.0%)
- Carol White: 8 (16.0%)
- Henry Moore: 7 (14.0%)
- Jack Anderson: 4 (8.0%)
- Isabella Taylor: 4 (8.0%)
### product_id (top 5 of 5 unique values)
- P004: 14 (28.0%)
- P003: 12 (24.0%)
- P002: 8 (16.0%)
- P005: 8 (16.0%)
- P001: 8 (16.0%)
### product_name (top 5 of 6 unique values)
- Monitor: 14 (28.0%)
- Keyboard: 12 (24.0%)
- Mouse: 8 (16.0%)
- Laptop: 8 (16.0%)
- Headphones: 7 (14.0%)
### store_id (top 3 of 3 unique values)
- S1: 18 (36.0%)
- S2: 17 (34.0%)
- S3: 15 (30.0%)

## Top Correlations
- unit_price vs total_price: r = 0.912
- quantity vs total_price: r = 0.373
- unit_price vs quantity: r = -0.035

## Chart Index
- overview_numeric_distributions.png (overview)
- correlation_heatmap.png (correlation)
- distribution_unit_price.png (distribution)
- distribution_quantity.png (distribution)
- distribution_total_price.png (distribution)
- category_order_id.png (category)
- category_customer_id.png (category)
- category_customer_name.png (category)
- category_product_id.png (category)
- category_product_name.png (category)
- category_store_id.png (category)
- category_store_name.png (category)
- category_city.png (category)
- time_series_unit_price.png (time)
- time_series_quantity.png (time)
- time_series_total_price.png (time)
- overview_scatter_unit_price_vs_total_price.png (overview)

## Caveats
- This report is exploratory. Observed patterns should be validated before drawing conclusions.
- Missingness and data quality may influence results.
