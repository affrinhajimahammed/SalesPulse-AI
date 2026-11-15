# SalesPulse AI
### Intelligent Sales Forecasting & Pipeline Risk Management

SalesPulse AI is a sales forecasting and pipeline risk management application. It analyzes sales opportunities, estimates expected revenue, compares forecast scenarios, identifies risky deals, and tracks historical forecasts.

## 1. Problem Statement

Sales teams need better visibility into their sales pipeline to estimate future bookings and identify opportunities that may not close on time.

SalesPulse AI uses opportunity amounts, conversion probabilities, opportunity age, and sales activity data to generate forecasts and highlight pipeline risks.

## 2. Key Features

- Sales pipeline analysis
- Weighted revenue forecasting
- Best-case, expected, and worst-case scenarios
- What-if scenario simulator
- Opportunity stage filtering
- Opportunity ageing analysis
- Rule-based pipeline risk detection
- Sales representative and territory analysis
- Forecast history storage and retrieval
- Synthetic dataset generation
- Separate labelled anomaly dataset
- CSV and JSON data exports
- Forecast evaluation metric functions (MAE and WAPE)

## 3. Technology Stack

- Python
- Streamlit
- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- Pytest

## 4. Project Structure

```text
SalesPulse-AI/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── validation.py
│   ├── forecasting.py
│   └── services/
│       ├── opportunity_service.py
│       ├── forecast_service.py
│       ├── audit_service.py
│       └── risk_service.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── generator.py
│   ├── export_data.py
│   ├── anomaly_generator.py
│   └── generator_backup.py
│
├── tests/
│   └── test_forecasting.py
│
├── exports/
│   ├── salespulse_dataset.json
│   ├── anomalies.csv
│   └── anomaly_labels.csv
│
├── requirements.txt
├── DATA_DICTIONARY.md
├── SOURCE_MANIFEST.md
├── salespulse.db
└── README.md
```

## 5. Dataset

The synthetic baseline dataset was generated using a fixed random seed: `20261022`.

| Entity | Records |
|---|---:|
| Sales Representatives | 2,000 |
| Accounts | 2,000 |
| Opportunities | 20,000 |
| Stage History | 60,975 |
| Activities | 60,225 |
| Quotas | 16,000 |
| Historical Bookings | 3,962 |
| Forecast Snapshots | 8 |

The baseline dataset passed the generator's validation checks with zero reported errors.

### Anomaly Dataset

Five separate labelled test anomalies were generated:

1. Negative opportunity amount
2. Invalid conversion probability
3. Close date before creation date
4. Missing account reference
5. Mixed currency

Anomaly records are stored separately from the baseline dataset in `anomalies.csv` and `anomaly_labels.csv`. They are illustrative test cases and do not modify the baseline data.

## 6. Installation and Setup

### Step 1: Clone or download the project

Open the project folder in VS Code.

### Step 2: Install dependencies

Run this command in the project terminal:

```bash
pip install -r requirements.txt
```

### Step 3: Start the backend API

```bash
python -m uvicorn backend.main:app --reload
```

### Step 4: Open API documentation

Visit:

http://127.0.0.1:8000/docs

### Step 5: Start the Streamlit dashboard

Open a second terminal and run:

```bash
python -m streamlit run frontend/app.py
```

### Step 6: Open the dashboard

Visit:

http://localhost:8501

## 7. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API home |
| GET | `/health` | Health check |
| POST | `/forecast` | Generate forecast |
| POST | `/risks` | Detect pipeline risks |
| POST | `/forecast-history` | Save forecast snapshot |
| GET | `/forecast-history` | Retrieve forecast history |

## 8. Forecasting Method

Weighted pipeline revenue is calculated as:

**Weighted Revenue = Opportunity Amount × (Probability / 100)**

The application currently uses illustrative scenario adjustments:

- Worst case: Expected revenue × 0.80
- Expected case: Weighted pipeline revenue
- Best case: Expected revenue × 1.20

These adjustments are illustrative assumptions, not statistically calibrated confidence intervals.

## 9. Pipeline Risk Detection

The application uses rule-based conditions to identify potentially risky opportunities.

Current rules include:

- Opportunity open for 60 days or more
- Conversion probability of 25% or lower

Risk classification:

- **High Risk:** Both conditions are met.
- **Medium Risk:** One condition is met.
- **Low Risk:** Neither condition is met.

These are business rules, not predictions from a trained machine learning model.

## 10. Forecast Evaluation Metrics

The forecasting module includes reusable functions for:

- Mean Absolute Error (MAE)
- Weighted Absolute Percentage Error (WAPE)
- Group-based forecast evaluation

These functions are available for evaluation, but a complete historical forecast accuracy evaluation by horizon and segment has not yet been integrated into the application.

## 11. Testing

Run the project tests using:

```bash
python -m pytest -v
```

The current test suite contains seven tests covering forecasting calculations, input validation, evaluation metrics, and empty or mismatched inputs.

## 12. Data Generation and Reproducibility

Generate the synthetic baseline dataset and exports using:

```bash
python -m data.export_data
```

Generate the separate anomaly dataset using:

```bash
python -m data.anomaly_generator
```

The fixed seed `20261022` supports repeatable synthetic data generation.

Refer to `DATA_DICTIONARY.md` for field descriptions and `SOURCE_MANIFEST.md` for dataset counts, validation information, and reproducibility details.

## 13. Current Limitations

- Scenario adjustments use fixed illustrative percentages rather than calibrated uncertainty intervals.
- Risk detection currently uses business rules instead of a trained machine learning model.
- MAE and WAPE functions are implemented but are not yet integrated into a complete historical forecast evaluation workflow.
- The Streamlit dashboard uses a smaller sample opportunity dataset, while the full-scale synthetic dataset is available separately in the exports folder.
- The generator's validation checks do not constitute exhaustive validation of every business rule or data-quality edge case.

## 14. Future Enhancements

- Integrate historical forecast accuracy evaluation by forecast horizon and business segment.
- Improve scenario estimation using historical forecast errors.
- Develop predictive models for opportunity slippage and pipeline risk.
- Expand data-quality checks and anomaly detection.
- Integrate the full-scale dataset into the interactive dashboard.

---

**SalesPulse AI — Intelligent Sales Forecasting & Pipeline Risk Management**