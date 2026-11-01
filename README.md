# Bank Customer Churn Analysis Dashboard

A Streamlit dashboard for exploring customer churn across geography, age, tenure, balance, and engagement. It uses the included cleaned CSV by default and lets you upload a compatible CSV to use instead for the current session.

## Features

- Customer count, churned customer count, churn rate, and retention rate
- Geography filter that updates the dashboard summaries
- Churn charts by geography, age group, tenure group, and active-member status
- High-value customer summary and churn by geography
- Customer-level drill-down table
- CSV upload with required-column and numeric-value checks

## Project files

- `app.py` - Streamlit application
- `European_Bank_Cleaned.csv` - default dashboard dataset
- `European_Bank.csv` - original dataset
- `Untitled.ipynb` - analysis notebook
- `churn_model.pkl` and `model_columns.pkl` - saved model artifacts
- `requirements.txt` - pinned Python dependencies

The dashboard currently presents descriptive analysis from the CSV data. The saved model artifacts are included in the repository but are not loaded by the dashboard.

## Requirements

- Python 3.14
- The packages listed in `requirements.txt`

## Use another dataset

In the dashboard sidebar, under **Dataset**, upload a CSV. The uploaded file is used for that dashboard session. Remove it to switch back to `European_Bank_Cleaned.csv`.

The CSV must contain these columns:

| Column | Expected values |
| --- | --- |
| `Geography` | Customer geography/category |
| `Gender` | Customer gender/category |
| `Age` | Numeric |
| `CreditScore` | Numeric |
| `Tenure` | Numeric |
| `Balance` | Numeric |
| `NumOfProducts` | Numeric |
| `IsActiveMember` | Numeric, typically 0 or 1 |
| `EstimatedSalary` | Numeric |
| `Exited` | 0 for retained customers, 1 for churned customers |

Numeric fields must not contain blanks or non-numeric values. The app creates `Age_Group`, `Credit_Score_Band`, `Tenure_Group`, `Balance_Segment`, and `High_Value` when those columns are not already present.
