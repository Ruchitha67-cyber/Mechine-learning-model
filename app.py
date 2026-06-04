import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="🚀 Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# -------------------------------------------------
# Custom Styling
# -------------------------------------------------

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

[data-testid="metric-container"] {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 10px;
}

h1 {
    color: #2563eb;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("🚀 Startup Analytics Dashboard")
st.markdown("### Deep Analytics & Business Insights")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("📌 Filters")

industry = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# -------------------------------------------------
# KPI Section
# -------------------------------------------------

total_startups = len(filtered_df)
total_funding = filtered_df["Funding Amount (M USD)"].sum()
avg_revenue = filtered_df["Revenue (M USD)"].mean()
avg_valuation = filtered_df["Valuation (M USD)"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Startups", total_startups)
c2.metric("Funding Raised", f"${total_funding:,.0f}M")
c3.metric("Average Revenue", f"${avg_revenue:,.1f}M")
c4.metric("Average Valuation", f"${avg_valuation:,.1f}M")

st.divider()

# -------------------------------------------------
# Charts Row 1
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    funding_by_industry = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        funding_by_industry,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    valuation_by_region = (
        filtered_df.groupby("Region")
        ["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        valuation_by_region,
        names="Region",
        values="Valuation (M USD)",
        title="Regional Valuation Share"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Revenue vs Valuation
# -------------------------------------------------

st.subheader("📈 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    size="Employees",
    color="Industry",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Top Startups
# -------------------------------------------------

st.subheader("🏆 Top Startups by Valuation")

top_startups = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_startups,
    use_container_width=True
)

# -------------------------------------------------
# Insights
# -------------------------------------------------

st.subheader("🧠 Business Insights")

top_industry = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

st.success(
    f"🏆 Highest Valuation Industry: {top_industry}"
)

st.info(
    f"🌍 Top Funding Region: {top_region}"
)

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------

with st.expander("📂 View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# -------------------------------------------------
# Download Data
# -------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name="startup_analysis.csv",
    mime="text/csv"
)
