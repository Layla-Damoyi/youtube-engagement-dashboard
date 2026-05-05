import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG + DARK STYLE
# -----------------------------
st.set_page_config(page_title="YouTube Analytics", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 YouTube Analytics Dashboard")
st.caption("Interactive insights from your YouTube data")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("Table data.csv")
chart = pd.read_csv("Chart data.csv")

df.columns = df.columns.str.strip()
chart.columns = chart.columns.str.strip()

# Clean
if "Content" in df.columns:
    df = df[df["Content"] != "Total"]

# Convert numbers
cols = ["Views", "Watch time (hours)", "Impressions click-through rate (%)"]
for col in cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# DATE FILTER (INTERACTIVE)
# -----------------------------
st.sidebar.header("📅 Filter by Date")

date_col = chart.columns[0]
chart[date_col] = pd.to_datetime(chart[date_col])

start_date = st.sidebar.date_input("Start Date", chart[date_col].min())
end_date = st.sidebar.date_input("End Date", chart[date_col].max())

filtered_chart = chart[
    (chart[date_col] >= pd.to_datetime(start_date)) &
    (chart[date_col] <= pd.to_datetime(end_date))
]

# -----------------------------
# VIRAL SCORE
# -----------------------------
df["Viral Score"] = (
    df["Views"] *
    df["Watch time (hours)"] *
    df["Impressions click-through rate (%)"]
)

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📈 Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Total Views", int(df["Views"].sum()))
c2.metric("Avg CTR", round(df["Impressions click-through rate (%)"].mean(), 2))
c3.metric("Top Viral Score", int(df["Viral Score"].max()))

# -----------------------------
# BAR GRAPH (Top Videos)
# -----------------------------
st.subheader("🔥 Most Viral Videos")

top = df.sort_values("Viral Score", ascending=False).head(5)

fig, ax = plt.subplots()
colors = ["#6366F1", "#22C55E", "#F59E0B", "#EF4444", "#0EA5E9"]
ax.barh(top["Video title"], top["Viral Score"], color=colors)

ax.set_facecolor("#0e1117")
fig.patch.set_facecolor("#0e1117")

st.pyplot(fig)

# -----------------------------
# LINE GRAPH (TREND)
# -----------------------------
st.subheader("📈 Views Over Time")

value_col = filtered_chart.columns[1]

fig2, ax2 = plt.subplots()
ax2.plot(filtered_chart[date_col], filtered_chart[value_col])

ax2.set_facecolor("#0e1117")
fig2.patch.set_facecolor("#0e1117")

plt.xticks(rotation=45)
st.pyplot(fig2)

# -----------------------------
# SCATTER (ENGAGEMENT)
# -----------------------------
st.subheader("📊 Views vs Watch Time")

fig3, ax3 = plt.subplots()
ax3.scatter(df["Views"], df["Watch time (hours)"])

ax3.set_facecolor("#0e1117")
fig3.patch.set_facecolor("#0e1117")

st.pyplot(fig3)

st.caption("Built with Python, Pandas, Matplotlib & Streamlit")