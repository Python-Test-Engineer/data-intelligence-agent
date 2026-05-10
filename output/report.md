# CSV Dataset Report

## Dataset Snapshot
- Rows: 110527
- Columns: 14
- Numeric columns: 9
- Categorical columns: 5
- Missing cells: 0

## Numeric Summary
- **patientid**: mean=147496265710394.06, std=256094920291739.09, min=39217.84, max=999981631772427.00, median=31731838713978.00
- **appointmentid**: mean=5675305.12, std=71295.75, min=5030230.00, max=5790484.00, median=5680573.00
- **age**: mean=37.09, std=23.11, min=-1.00, max=115.00, median=37.00
- **scholarship**: mean=0.10, std=0.30, min=0.00, max=1.00, median=0.00
- **hipertension**: mean=0.20, std=0.40, min=0.00, max=1.00, median=0.00
- **diabetes**: mean=0.07, std=0.26, min=0.00, max=1.00, median=0.00
- **alcoholism**: mean=0.03, std=0.17, min=0.00, max=1.00, median=0.00
- **handcap**: mean=0.02, std=0.16, min=0.00, max=4.00, median=0.00

## Top Category Distributions
### gender (top 2 of 2 unique values)
- F: 71840 (65.0%)
- M: 38687 (35.0%)
### appointmentday (top 5 of 27 unique values)
- 2016-06-06T00:00:00Z: 4692 (4.2%)
- 2016-05-16T00:00:00Z: 4613 (4.2%)
- 2016-05-09T00:00:00Z: 4520 (4.1%)
- 2016-05-30T00:00:00Z: 4514 (4.1%)
- 2016-06-08T00:00:00Z: 4479 (4.1%)
### no_show (top 2 of 2 unique values)
- No: 88208 (79.8%)
- Yes: 22319 (20.2%)

## Top Correlations
- age vs hipertension: r = 0.505
- hipertension vs diabetes: r = 0.433
- age vs diabetes: r = 0.292
- appointmentid vs sms_received: r = -0.257
- age vs alcoholism: r = 0.096

## Chart Index
- overview_numeric_distributions.png (overview)
- correlation_heatmap.png (correlation)
- distribution_patientid.png (distribution)
- distribution_appointmentid.png (distribution)
- distribution_age.png (distribution)
- distribution_scholarship.png (distribution)
- distribution_hipertension.png (distribution)
- distribution_diabetes.png (distribution)
- category_gender.png (category)
- category_appointmentday.png (category)
- category_no_show.png (category)
- overview_scatter_age_vs_hipertension.png (overview)

## Caveats
- This report is exploratory. Observed patterns should be validated before drawing conclusions.
- Missingness and data quality may influence results.
