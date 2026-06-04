import streamlit as st
import pandas as pd

st.title("🤖 Machine Learning Analytics")

st.markdown("""
This page demonstrates how startup features influence valuation.

The dashboard uses:

- Funding Amount
- Revenue
- Employees

to estimate startup valuation.
""")

# Load data
df = pd.read_csv("startup_data.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Correlation Analysis
st.subheader("Feature Correlation")

corr = df[
    [
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Valuation (M USD)",
        "Employees"
    ]
].corr()

st.dataframe(corr)

# User Inputs
st.subheader("Valuation Estimator")

funding = st.slider(
    "Funding Amount (M USD)",
    0,
    500,
    100
)

revenue = st.slider(
    "Revenue (M USD)",
    0,
    200,
    30
)

employees = st.slider(
    "Employees",
    1,
    5000,
    500
)

# Simple analytical estimate
estimated_valuation = (
    funding * 3 +
    revenue * 10 +
    employees * 0.2
)

st.metric(
    "Estimated Valuation",
    f"${estimated_valuation:,.0f}M"
)

st.success(
    "This is an analytical valuation estimate for demonstration purposes."
)
