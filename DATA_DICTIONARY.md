
# SalesPulse AI – Data Dictionary

## Project Overview
SalesPulse AI is a synthetic sales forecasting and pipeline risk management project.

The dataset contains sales representatives, territories, accounts, opportunities, activities, stage history, quotas, historical bookings, and forecast snapshots.

Currency: INR.

## 1. Territories
File: territories.csv

| Column | Description |
|---|---|
| territory_id | Unique territory ID |
| name | Territory name |

## 2. Sales Representatives
File: sales_reps.csv

| Column | Description |
|---|---|
| rep_id | Unique representative ID |
| name | Representative name |
| territory_id | Assigned territory ID |

## 3. Accounts
File: accounts.csv

| Column | Description |
|---|---|
| account_id | Unique account ID |
| company_name | Customer company name |
| industry | Customer industry |
| territory_id | Associated territory ID |

## 4. Stages
File: stages.csv

| Column | Description |
|---|---|
| stage_id | Unique stage ID |
| name | Opportunity stage |
| probability | Default win probability percentage |

## 5. Opportunities
File: opportunities.csv

| Column | Description |
|---|---|
| id | Unique opportunity ID |
| name | Opportunity name |
| account | Account name |
| account_id | Associated account ID |
| amount | Opportunity amount |
| currency | Currency code |
| stage | Current opportunity stage |
| stage_id | Associated stage ID |
| probability | Estimated win probability |
| created_date | Opportunity creation date |
| expected_close_date | Expected closing date |
| days_open | Number of days since creation |
| product | Associated product |
| sales_rep | Representative name |
| sales_rep_id | Representative ID |
| territory | Territory name |
| territory_id | Territory ID |

## 6. Stage History
File: stage_history.csv

| Column | Description |
|---|---|
| id | Unique history event ID |
| opportunity_id | Associated opportunity ID |
| old_stage | Previous stage |
| new_stage | New stage |
| changed_date | Date of stage change |

## 7. Activities
File: activities.csv

| Column | Description |
|---|---|
| activity_id | Unique activity ID |
| opportunity_id | Associated opportunity ID |
| sales_rep_id | Representative ID |
| activity_type | Type of sales activity |
| activity_date | Activity date |

## 8. Quotas
File: quotas.csv

| Column | Description |
|---|---|
| quota_id | Unique quota ID |
| sales_rep_id | Representative ID |
| period | Quarterly period |
| target_amount | Sales target |
| currency | Currency code |

## 9. Historical Bookings
File: historical_bookings.csv

| Column | Description |
|---|---|
| booking_id | Unique booking ID |
| opportunity_id | Associated opportunity ID |
| booking_date | Booking date |
| booking_amount | Actual booked amount |
| currency | Currency code |
| status | Booking status |

## 10. Forecast Snapshots
File: forecast_snapshots.csv

| Column | Description |
|---|---|
| snapshot_id | Unique forecast ID |
| snapshot_date | Forecast date |
| opportunity_count | Number of open opportunities |
| pipeline_amount | Total pipeline value |
| expected_revenue | Probability-weighted revenue |
| best_case | Illustrative best-case forecast |
| worst_case | Illustrative worst-case forecast |
| currency | Currency code |

## Data Generation Details

- Random seed: 20261022
- Data is synthetically generated.
- Generation is reproducible using the same seed.
- Current development dataset: 20 opportunities.
- Target dataset scale: 20,000 opportunities.
- CSV files are stored in the exports folder.
- Complete dataset is stored in salespulse_dataset.json.

## Important Notes

- Forecasts are estimates, not guaranteed revenue.
- Best-case and worst-case scenarios use illustrative assumptions.
- Synthetic data is used for development and testing.

## Full-Scale Dataset

The generated dataset uses a fixed random seed (20261022).

| Entity | Record Count |
|---|---:|
| Sales Representatives | 2,000 |
| Accounts | 2,000 |
| Territories | 3 |
| Opportunities | 20,000 |
| Stage History | 60,975 |
| Activities | 60,225 |
| Quotas | 16,000 |
| Historical Bookings | 3,962 |
| Forecast Snapshots | 8 |

## Anomaly Dataset

Anomalies are stored separately from the valid baseline dataset.

### anomalies.csv
Contains 5 intentionally invalid records:
- NEGATIVE_AMOUNT
- INVALID_PROBABILITY
- CLOSE_DATE_BEFORE_CREATION
- MISSING_ACCOUNT
- MIXED_CURRENCY

### anomaly_labels.csv
Contains the corresponding ground-truth labels:
- `label = 1`: Anomaly
- `is_anomaly = True`: Confirmed synthetic anomaly

The anomaly records are illustrative test cases and are not included in the baseline exports.
