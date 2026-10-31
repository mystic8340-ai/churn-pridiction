import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="European Bank Customer Churn",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 European Bank Customer Churn Analysis")

st.write(
    "Interactive dashboard for analyzing customer churn "
    "across geography, demographics, engagement and financial profiles."
)

st.sidebar.header("Dataset")
uploaded_dataset = st.sidebar.file_uploader(
    "Upload a replacement dataset (CSV)",
    type=["csv"],
    help="The uploaded CSV is used for this dashboard session. Remove it to return to the default dataset."
)

if uploaded_dataset is not None:
    dataset_name = uploaded_dataset.name
    try:
        df = pd.read_csv(uploaded_dataset)
    except Exception as error:
        st.error(f"Could not read {dataset_name}: {error}")
        st.stop()
else:
    default_dataset = Path(__file__).with_name("European_Bank_Cleaned.csv")
    dataset_name = default_dataset.name
    try:
        df = pd.read_csv(default_dataset)
    except Exception as error:
        st.error(f"Could not read the default dataset {dataset_name}: {error}")
        st.stop()

df.columns = df.columns.astype(str).str.strip()
required_columns = {
    "Geography",
    "Gender",
    "Age",
    "CreditScore",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
}
missing_columns = sorted(required_columns.difference(df.columns))
if missing_columns:
    st.error(
        f"{dataset_name} is missing required columns: "
        f"{', '.join(missing_columns)}."
    )
    st.info("Upload a CSV with the same customer fields as the default dataset.")
    st.stop()

if df.empty:
    st.error(f"{dataset_name} contains no customer rows.")
    st.stop()

numeric_columns = [
    "Age",
    "CreditScore",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

invalid_numeric_columns = [
    column for column in numeric_columns if df[column].isna().any()
]
if invalid_numeric_columns:
    st.error(
        "These fields must contain numeric values with no blanks: "
        f"{', '.join(invalid_numeric_columns)}."
    )
    st.stop()

if not df["Exited"].isin([0, 1]).all():
    st.error("The Exited column must contain only 0 (stayed) and 1 (churned).")
    st.stop()

# Add the dashboard categories when the cleaned CSV only contains raw fields.
if 'Age_Group' not in df.columns:
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 29, 45, 60, np.inf],
        labels=['<30', '30-45', '46-60', '60+']
    )

if 'Credit_Score_Band' not in df.columns:
    df['Credit_Score_Band'] = pd.cut(
        df['CreditScore'],
        bins=[0, 579, 699, np.inf],
        labels=['Low', 'Medium', 'High']
    )

if 'Tenure_Group' not in df.columns:
    df['Tenure_Group'] = pd.cut(
        df['Tenure'],
        bins=[-1, 3, 6, np.inf],
        labels=['New', 'Mid-term', 'Long-term']
    )

if 'Balance_Segment' not in df.columns:
    df['Balance_Segment'] = pd.cut(
        df['Balance'],
        bins=[-1, 0, 75000, np.inf],
        labels=['Zero-balance', 'Low-balance', 'High-balance']
    )

if 'High_Value' not in df.columns:
    high_value_threshold = df['Balance'].quantile(0.75)
    df['High_Value'] = np.where(
        df['Balance'] >= high_value_threshold,
        'High-Value',
        'Regular'
    )

st.success(f"Dataset loaded successfully: {dataset_name}")

st.write("Number of customers:", len(df))
total_customers = len(df)

churned_customers = int(df['Exited'].sum())

churn_rate = df['Exited'].mean() * 100

retention_rate = 100 - churn_rate

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churned Customers",
    f"{churned_customers:,}"
)

col3.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col4.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)
st.sidebar.header("Filters")

selected_geo = st.sidebar.multiselect(
    "Select Geography",
    options=sorted(df['Geography'].unique()),
    default=sorted(df['Geography'].unique())
)

filtered_df = df[
    df['Geography'].isin(selected_geo)
]
filtered_churn_rate = filtered_df['Exited'].mean() * 100

filtered_churned = int(filtered_df['Exited'].sum())

col1, col2 = st.columns(2)

col1.metric(
    "Filtered Customers",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Filtered Churn Rate",
    f"{filtered_churn_rate:.2f}%"
)
st.header("🌍 Churn by Geography")

geo_dashboard = filtered_df.groupby(
    'Geography'
)['Exited'].mean().reset_index()

geo_dashboard['Exited'] = (
    geo_dashboard['Exited'] * 100
)

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=geo_dashboard,
    x='Geography',
    y='Exited',
    ax=ax
)

ax.set_xlabel("Geography")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Geography")

st.pyplot(fig)
st.header("👥 Churn by Age Group")

age_dashboard = filtered_df.groupby(
    'Age_Group',
    observed=True
)['Exited'].mean().reset_index()

age_dashboard['Exited'] = (
    age_dashboard['Exited'] * 100
)

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=age_dashboard,
    x='Age_Group',
    y='Exited',
    ax=ax
)

ax.set_xlabel("Age Group")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Age Group")

st.pyplot(fig)
st.header("📅 Churn by Tenure")

tenure_dashboard = filtered_df.groupby(
    'Tenure_Group',
    observed=True
)['Exited'].mean().reset_index()

tenure_dashboard['Exited'] = (
    tenure_dashboard['Exited'] * 100
)

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=tenure_dashboard,
    x='Tenure_Group',
    y='Exited',
    ax=ax
)

ax.set_xlabel("Tenure Group")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Tenure Group")

st.pyplot(fig)
st.header("💰 High-Value Customer Analysis")

high_value_df = filtered_df[
    filtered_df['High_Value'] == 'High-Value'
]

high_value_churn_rate = (
    high_value_df['Exited'].mean() * 100
    if len(high_value_df) > 0
    else 0
)

col1, col2 = st.columns(2)

col1.metric(
    "High-Value Customers",
    f"{len(high_value_df):,}"
)

col2.metric(
    "High-Value Churn Rate",
    f"{high_value_churn_rate:.2f}%"
)
if len(high_value_df) > 0:

    hv_geo = high_value_df.groupby(
        'Geography'
    )['Exited'].mean().reset_index()

    hv_geo['Exited'] = hv_geo['Exited'] * 100

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=hv_geo,
        x='Geography',
        y='Exited',
        ax=ax
    )

    ax.set_title(
        'High-Value Customer Churn by Geography'
    )

    ax.set_xlabel('Geography')
    ax.set_ylabel('Churn Rate (%)')

    st.pyplot(fig)
    st.header("🔎 Customer Drill-Down")

display_columns = [
    'Geography',
    'Gender',
    'Age',
    'Age_Group',
    'CreditScore',
    'Credit_Score_Band',
    'Tenure',
    'Tenure_Group',
    'Balance',
    'Balance_Segment',
    'NumOfProducts',
    'IsActiveMember',
    'EstimatedSalary',
    'Exited'
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True
)
st.header("📊 Engagement vs Churn")

engagement_dashboard = filtered_df.groupby(
    'IsActiveMember'
)['Exited'].mean().reset_index()

engagement_dashboard['Exited'] = (
    engagement_dashboard['Exited'] * 100
)

engagement_dashboard['Status'] = (
    engagement_dashboard['IsActiveMember']
    .map({
        0: 'Inactive',
        1: 'Active'
    })
)

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=engagement_dashboard,
    x='Status',
    y='Exited',
    ax=ax
)

ax.set_xlabel("Customer Engagement")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate: Active vs Inactive Customers")

st.pyplot(fig)
