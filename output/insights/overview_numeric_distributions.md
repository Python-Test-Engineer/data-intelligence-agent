# Insights: Overview Numeric Distributions

![overview_numeric_distributions.png](../images/overview_numeric_distributions.png)

## Data Insight
- The box plot reveals that 'patientid' has an extremely wide range of values, with a median close to zero and a very high upper whisker. All other numeric columns show very small, tightly clustered distributions, with medians at or near zero.

## Analysis Insight
- The 'patientid' column's distribution is drastically different from all others. This suggests 'patientid' and 'appointmentid' are likely identifiers, not quantitative variables, while 'age', 'scholarship', 'hipertension', 'diabetes', 'alcoholism', 'handcap', and 'sms_received' are binary or categorical, represented numerically.

## Caveat
- The 'patientid' and 'appointmentid' columns are extremely large and likely contain IDs rather than measurable quantities. Their distributions distort the overall view. Analysis should focus on the other columns, treating them as categorical or binary indicators.
