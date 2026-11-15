
# SalesPulse AI – Source Manifest

## 1. Project Information

- Project Name: SalesPulse AI
- Purpose: Intelligent Sales Forecasting and Pipeline Risk Management
- Dataset Type: Synthetic Sales Data
- Generation Language: Python
- Random Seed: 20261022
- Currency: INR
- Reference Date: 2026-11-15

## 2. Data Source

All records are generated programmatically using:

`data/generator.py`

No real customer, company, or financial records are used.

## 3. Generated Entities

| Entity | Description |
|---|---|
| Territories | Sales operating regions |
| Sales Representatives | Sales team members |
| Accounts | Synthetic customer companies |
| Stages | Opportunity sales stages |
| Opportunities | Sales deals and their values |
| Stage History | Opportunity stage transitions |
| Activities | Sales representative activities |
| Quotas | Quarterly sales targets |
| Historical Bookings | Closed-won booking records |
| Forecast Snapshots | Historical forecast calculations |

## 4. Export Files

Generated files are stored in the `exports/` directory.

- salespulse_dataset.json
- territories.csv
- sales_reps.csv
- accounts.csv
- stages.csv
- opportunities.csv
- stage_history.csv
- activities.csv
- quotas.csv
- historical_bookings.csv
- forecast_snapshots.csv

## 5. Reproducibility

To regenerate the dataset, run:

`python -m data.export_data`

The generator uses a fixed random seed of 20261022.

Running the generator with the same seed and configuration produces identical data.

## 6. Validation

The generator includes checks for selected data quality rules, including:

- Valid account references
- Valid sales representative references
- Valid opportunity amounts
- Valid probability ranges
- Valid historical booking references
- Valid stage history references

The current development dataset passed these checks.

## 7. Dataset Scale

Current development dataset:

- 20 opportunities
- 4 sales representatives
- 15 accounts
- 3 territories
- 32 quotas
- 8 forecast snapshots

Target hackathon scale:

- 2,000 sales representatives
- 2,000 accounts
- 20,000 opportunities
- 8 quarters of forecast snapshots

The current development dataset has not yet reached the target scale.

## Full-Scale Generation Results

- Random seed: 20261022
- Sales representatives: 2,000
- Accounts: 2,000
- Opportunities: 20,000
- Stage history records: 60,975
- Activity records: 60,225
- Quota records: 16,000
- Historical bookings: 3,962
- Forecast snapshots: 8
- Baseline validation: PASSED
- Validation errors: 0

## Anomaly Generation

Generated separately using `data/anomaly_generator.py`.

Output files:
- `exports/anomalies.csv`
- `exports/anomaly_labels.csv`

Five labelled synthetic anomaly cases:
1. Negative amount
2. Invalid probability
3. Close date before creation
4. Missing account reference
5. Mixed currency

Anomaly records are separate from the valid baseline dataset.

## Reproducibility

The baseline dataset is generated using a fixed seed of 20261022.
Run `python -m data.export_data` to regenerate the baseline exports.
Run `python -m data.anomaly_generator` to regenerate the anomaly files.
