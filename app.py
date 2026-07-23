import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Data Observability", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/dq_metrics.csv", parse_dates=["date"])
    return df

df = load_data()

st.title("📊 Data Observability Dashboard")
st.caption("Simulated data quality metrics — Completeness, Timeliness, Uniqueness, Overall Health")

# Sidebar filters
tables = sorted(df["table_name"].unique())
selected_tables = st.sidebar.multiselect("Tables", tables, default=tables)
filtered = df[df["table_name"].isin(selected_tables)]

# Top-line KPIs (most recent day, averaged across selected tables)
latest_date = filtered["date"].max()
latest = filtered[filtered["date"] == latest_date]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall Health", f"{latest['overall_health_score'].mean():.1f}")
col2.metric("Completeness", f"{latest['completeness_score'].mean():.1f}")
col3.metric("Timeliness", f"{latest['timeliness_score'].mean():.1f}")
col4.metric("Uniqueness", f"{latest['uniqueness_score'].mean():.1f}")

st.divider()

# Trend chart
metric = st.selectbox(
    "Metric to trend",
    ["overall_health_score", "completeness_score", "timeliness_score", "uniqueness_score"],
    format_func=lambda x: x.replace("_", " ").title(),
)
fig = px.line(
    filtered, x="date", y=metric, color="table_name",
    title=f"{metric.replace('_', ' ').title()} over time",
)
st.plotly_chart(fig, use_container_width=True)

# Table-level snapshot
st.subheader("Latest scores by table")
snapshot = (
    latest[["table_name", "completeness_score", "timeliness_score", "uniqueness_score", "overall_health_score", "row_count"]]
    .sort_values("overall_health_score")
    .reset_index(drop=True)
)
st.dataframe(snapshot, use_container_width=True)
