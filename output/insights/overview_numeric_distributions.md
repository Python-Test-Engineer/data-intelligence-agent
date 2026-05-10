# Insights: Overview Numeric Distributions

![overview_numeric_distributions.png](../images/overview_numeric_distributions.png)

## Data Insight
- The 'patientid' column exhibits extreme variability in its values, with a mean around 1.47e15 and a very large standard deviation. The other numeric columns ('appointmentid', 'age', 'scholarship', 'hipertension', 'diabetes', 'alcoholism', 'handcap', 'sms_received') show much smaller and more concentrated distributions, with 'age' having the largest spread among them.

## Analysis Insight
- The box plot clearly highlights that 'patientid' and 'appointmentid' are identifiers with very large numerical ranges, while 'age' and binary/categorical features like 'scholarship', 'hipertension', 'diabetes', 'alcoholism', 'handcap', and 'sms_received' have small, near-zero values when represented numerically. This suggests distinct data types and scales within the dataset.

## Caveat
- The box plot for 'patientid' appears truncated on the y-axis, potentially obscuring extreme outliers or the full range of its distribution. The extremely large values in 'patientid' and 'appointmentid' are likely identifiers and not intended for direct quantitative analysis or comparison with other features.
