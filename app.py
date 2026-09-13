import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Page Configuration
st.set_page_config(
    page_title="SalesPulse | Enterprise Sales Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-fidelity CSS replicating exact theme, typography, colors and card styles from reference image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main background */
    .stApp {
        background-color: #F4F6FA;
    }

    /* Dark Navy Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B132B !important;
        color: #E2E8F0 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #94A3B8 !important;
        font-weight: 500;
        font-size: 13px;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    
    /* Brand logo in sidebar */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 4px 20px 4px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    .brand-icon {
        background: #0D9488;
        color: #FFFFFF;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-weight: 800;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.35);
    }
    .brand-text {
        color: #FFFFFF !important;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }

    /* Active Nav pill */
    .nav-pill-active {
        background: #0D9488;
        color: #FFFFFF !important;
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25);
    }

    /* Sidebar bottom upgrade box */
    .sidebar-upgrade-card {
        background: linear-gradient(135deg, #0D9488 0%, #0284C7 100%);
        border-radius: 14px;
        padding: 18px;
        color: #FFFFFF;
        margin-top: 24px;
        box-shadow: 0 8px 24px rgba(13, 148, 136, 0.25);
    }
    .sidebar-upgrade-card h4 {
        color: #FFFFFF !important;
        margin: 0 0 6px 0;
        font-size: 15px;
        font-weight: 700;
    }
    .sidebar-upgrade-card p {
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 12px !important;
        margin: 0 0 12px 0;
        line-height: 1.4;
    }
    .sidebar-upgrade-btn {
        background: #FFFFFF;
        color: #0F172A;
        font-weight: 700;
        font-size: 12px;
        padding: 8px 14px;
        border-radius: 8px;
        display: inline-block;
        text-align: center;
        width: 100%;
        border: none;
    }

    /* Top Greeting & Header Bar */
    .top-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        flex-wrap: wrap;
        gap: 16px;
    }
    .greeting-title {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin: 0 0 4px 0;
        letter-spacing: -0.5px;
    }
    .greeting-sub {
        font-size: 14px;
        color: #64748B;
        margin: 0;
        font-weight: 500;
    }
    .date-pill {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 600;
        color: #1E293B;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    /* KPI Cards exact replication */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-bottom: 24px;
    }
    @media (max-width: 1024px) {
        .kpi-row { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 640px) {
        .kpi-row { grid-template-columns: 1fr; }
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02), 0 1px 2px rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        transition: all 0.2s ease;
    }
    .kpi-card:hover {
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
        transform: translateY(-2px);
    }
    .kpi-content {
        display: flex;
        flex-direction: column;
    }
    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .kpi-delta {
        font-size: 12px;
        font-weight: 600;
        color: #10B981;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .kpi-icon-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }
    .icon-teal { background: #E6FFFA; color: #0D9488; }
    .icon-navy { background: #EEF2FF; color: #3B82F6; }
    .icon-coral { background: #FFF1F2; color: #F43F5E; }
    .icon-cyan { background: #ECFEFF; color: #0891B2; }

    /* Clean Card Container */
    .analytics-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02), 0 1px 2px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    .card-header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .card-link {
        font-size: 12px;
        font-weight: 600;
        color: #0D9488;
        cursor: pointer;
        text-decoration: none;
    }

    /* Deals Pipeline Funnel Stages styling */
    .funnel-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        margin-bottom: 16px;
    }
    @media (max-width: 900px) {
        .funnel-container { grid-template-columns: 1fr; }
    }
    .funnel-stage-col {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        background: #F8FAFC;
    }
    .funnel-stage-header {
        padding: 8px 10px;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 11px;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .funnel-stage-body {
        padding: 10px 8px;
    }
    .funnel-stage-amt {
        font-size: 14px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 8px;
        white-space: nowrap;
    }
    .funnel-deal-item {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 6px 8px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .funnel-deal-name {
        font-weight: 600;
        color: #1E293B;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 85px;
    }
    .funnel-deal-val {
        font-weight: 700;
        color: #0D9488;
        font-size: 11px;
    }

    /* Leaderboard Rep item */
    .rep-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #F1F5F9;
    }
    .rep-profile {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .rep-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #0D9488;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .rep-name {
        font-weight: 600;
        font-size: 13px;
        color: #1E293B;
    }
    .rep-progress-bar {
        background: #E2E8F0;
        border-radius: 999px;
        height: 6px;
        width: 90px;
        overflow: hidden;
        margin: 0 12px;
    }
    .rep-progress-fill {
        background: #0D9488;
        height: 100%;
        border-radius: 999px;
    }
    .rep-stats {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .rep-val {
        font-weight: 700;
        font-size: 13px;
        color: #0F172A;
    }
    .rep-pct {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        min-width: 38px;
        text-align: right;
    }

    /* Streamlit overrides for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
        padding: 0;
        margin-bottom: 16px;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        color: #64748B;
        font-weight: 600;
        font-size: 14px;
        border: none;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #0D9488 !important;
        border-bottom: 2px solid #0D9488 !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_sales_data():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "sales_data.csv")
    if not os.path.exists(csv_path):
        from generate_data import generate_synthetic_sales_data
        generate_synthetic_sales_data(output_path=csv_path)
    df = pd.read_csv(csv_path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])
    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Year"] = df["Order_Date"].dt.year
    return df

df_master = load_sales_data()

# ----------------- SIDEBAR: Dark Navy with Teal Accents -----------------
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <div class="brand-icon">⚡</div>
        <div class="brand-text">SalesPulse</div>
    </div>
    <div class="nav-pill-active">
        <span>📊</span>
        <span>Dashboard</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ **Filters & Scope**")

    # Date Filter
    min_d = df_master["Order_Date"].min().date()
    max_d = df_master["Order_Date"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
    else:
        start_d, end_d = min_d, max_d

    # Region Filter
    regions_list = sorted(df_master["Region"].unique())
    selected_regions = st.multiselect("Regions", options=regions_list, default=regions_list)

    # Category Filter
    cat_list = sorted(df_master["Category"].unique())
    selected_cats = st.multiselect("Categories", options=cat_list, default=cat_list)

    # Customer Segment Filter
    seg_list = sorted(df_master["Segment"].unique())
    selected_segs = st.multiselect("Customer Segments", options=seg_list, default=seg_list)

    # Reset
    if st.button("↺ Reset Filters", use_container_width=True):
        st.rerun()

    # Upgrade / Insights Card (Styled like bottom left widget in image)
    st.markdown("""
    <div class="sidebar-upgrade-card">
        <h4>Upgrade to Pro</h4>
        <p>Unlock predictive AI forecasting, deep automation, and custom exports.</p>
        <div class="sidebar-upgrade-btn">Upgrade Now →</div>
    </div>
    """, unsafe_allow_html=True)

# Filter Data
filtered_df = df_master[
    (df_master["Order_Date"].dt.date >= start_d) &
    (df_master["Order_Date"].dt.date <= end_d) &
    (df_master["Region"].isin(selected_regions)) &
    (df_master["Category"].isin(selected_cats)) &
    (df_master["Segment"].isin(selected_segs))
]

if filtered_df.empty:
    st.warning("No sales transactions found for the selected filter combination.")
    st.stop()

# ----------------- TOP GREETING BAR -----------------
st.markdown(f"""
<div class="top-header-row">
    <div>
        <h1 class="greeting-title">Welcome back, Alex! 👋</h1>
        <p class="greeting-sub">Here's what's happening with your sales performance and pipeline today.</p>
    </div>
    <div class="date-pill">
        <span>📅</span>
        <span>{start_d.strftime('%b %d, %Y')} – {end_d.strftime('%b %d, %Y')}</span>
        <span style="color:#0D9488; margin-left: 6px;">⚡ Filtered</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- 4 TOP KPI CARDS (Matching Image Exactly) -----------------
rev_total = filtered_df["Sales"].sum()
profit_total = filtered_df["Profit"].sum()
orders_total = len(filtered_df)
sales_target = 1600000.0
target_pct = min(100.0, (rev_total / sales_target) * 100)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Total Volume</span>
<span class="kpi-value">{filtered_df['Quantity'].sum():,}</span>
<span class="kpi-delta">↑ 18.6% vs last period</span>
</div>
<div class="kpi-icon-circle icon-teal">👥</div>
</div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Orders Placed</span>
<span class="kpi-value">{orders_total:,}</span>
<span class="kpi-delta">↑ 12.4% vs last period</span>
</div>
<div class="kpi-icon-circle icon-navy">💼</div>
</div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Revenue (MTD)</span>
<span class="kpi-value">${rev_total:,.0f}</span>
<span class="kpi-delta">↑ 22.7% vs last month</span>
</div>
<div class="kpi-icon-circle icon-coral">💵</div>
</div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Sales Target</span>
<span class="kpi-value">{target_pct:.0f}%</span>
<span class="kpi-delta" style="color: #64748B;">${rev_total/1000:,.0f}K / ${sales_target/1000:,.0f}K</span>
</div>
<div class="kpi-icon-circle icon-cyan">🎯</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ----------------- SECTION 1: DEALS PIPELINE & SALES TARGET PROGRESS -----------------
col_sec1_left, col_sec1_right = st.columns([1.65, 1.35])

with col_sec1_left:
    st.markdown("""<div class="analytics-card">
<div class="card-header-flex">
<h3 class="card-title">Deals Pipeline</h3>
<span class="card-link">Live Status</span>
</div>
<div class="funnel-container">
<div class="funnel-stage-col">
<div class="funnel-stage-header" style="background:#0D9488;">
<span>Prospecting</span>
<span style="font-size:11px; opacity:0.9;">18 Deals</span>
</div>
<div class="funnel-stage-body">
<div class="funnel-stage-amt">$215,000</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">BrightWave Ltd.</span>
<span class="funnel-deal-val">$25k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Summit Agency</span>
<span class="funnel-deal-val">$15k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">HexaTech Co.</span>
<span class="funnel-deal-val">$18k</span>
</div>
</div>
</div>
<div class="funnel-stage-col">
<div class="funnel-stage-header" style="background:#3B82F6;">
<span>Qualification</span>
<span style="font-size:11px; opacity:0.9;">22 Deals</span>
</div>
<div class="funnel-stage-body">
<div class="funnel-stage-amt">$310,000</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">TerraFirma Inc.</span>
<span class="funnel-deal-val">$30k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">BluePeak Corp.</span>
<span class="funnel-deal-val">$22k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Nova Systems</span>
<span class="funnel-deal-val">$28k</span>
</div>
</div>
</div>
<div class="funnel-stage-col">
<div class="funnel-stage-header" style="background:#1E3A8A;">
<span>Proposal</span>
<span style="font-size:11px; opacity:0.9;">16 Deals</span>
</div>
<div class="funnel-stage-body">
<div class="funnel-stage-amt">$240,000</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Vertex Solutions</span>
<span class="funnel-deal-val">$35k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">CloudScale</span>
<span class="funnel-deal-val">$20k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Insight Labs</span>
<span class="funnel-deal-val">$22k</span>
</div>
</div>
</div>
<div class="funnel-stage-col">
<div class="funnel-stage-header" style="background:#F43F5E;">
<span>Negotiation</span>
<span style="font-size:11px; opacity:0.9;">10 Deals</span>
</div>
<div class="funnel-stage-body">
<div class="funnel-stage-amt">$185,000</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Elite Ventures</span>
<span class="funnel-deal-val">$60k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Pioneer Corp.</span>
<span class="funnel-deal-val">$45k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">Alpha Networks</span>
<span class="funnel-deal-val">$40k</span>
</div>
</div>
</div>
<div class="funnel-stage-col">
<div class="funnel-stage-header" style="background:#10B981;">
<span>Closed Won</span>
<span style="font-size:11px; opacity:0.9;">20 Deals</span>
</div>
<div class="funnel-stage-body">
<div class="funnel-stage-amt">$512,000</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">GlobalLink Ltd.</span>
<span class="funnel-deal-val">$55k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">InnovateX</span>
<span class="funnel-deal-val">$45k</span>
</div>
<div class="funnel-deal-item">
<span class="funnel-deal-name">NextGen Digital</span>
<span class="funnel-deal-val">$68k</span>
</div>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

with col_sec1_right:
    # Monthly sales vs target progress chart (Matching right top chart in image)
    df_monthly = filtered_df.groupby("YearMonth")["Sales"].sum().reset_index().tail(10)
    monthly_target = df_monthly["Sales"].mean() * 1.15

    fig_target = go.Figure()
    fig_target.add_trace(go.Bar(
        x=df_monthly["YearMonth"],
        y=df_monthly["Sales"],
        name="Actual Sales",
        marker_color="#0D9488",
        marker_line_width=0,
        opacity=0.9
    ))
    fig_target.add_trace(go.Scatter(
        x=df_monthly["YearMonth"],
        y=[monthly_target] * len(df_monthly),
        name="Target Baseline",
        mode="lines",
        line=dict(color="#0284C7", dash="dash", width=2)
    ))
    fig_target.update_layout(
        template="plotly_white",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#64748B"),
        xaxis=dict(showgrid=False, linecolor="#E2E8F0"),
        yaxis=dict(gridcolor="#F1F5F9", showline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
    )

    st.markdown(f"""
    <div class="analytics-card">
        <div class="card-header-flex">
            <h3 class="card-title">Sales Target Progress</h3>
            <span style="font-size:12px; font-weight:700; color:#0D9488;">{target_pct:.0f}% Achieved</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:13px;">
            <div><span style="color:#64748B;">Target:</span> <b>${sales_target:,.0f}</b></div>
            <div><span style="color:#64748B;">Achieved:</span> <b style="color:#0D9488;">${rev_total:,.0f}</b></div>
            <div><span style="color:#64748B;">Remaining:</span> <b style="color:#F43F5E;">${max(0.0, sales_target - rev_total):,.0f}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_target, use_container_width=True)

# ----------------- SECTION 2: 3 COLUMNS (Category Donut, Team Leaderboard, Revenue Forecast) -----------------
c_left, c_mid, c_right = st.columns([1, 1, 1.1])

# Column 1: Category / Lead Share Donut
with c_left:
    st.markdown("""<div class="analytics-card" style="padding-bottom:12px;">
<div class="card-header-flex">
<h3 class="card-title">Revenue by Category</h3>
<span class="card-link">Breakdown</span>
</div>
</div>""", unsafe_allow_html=True)

    df_cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_donut = px.pie(
        df_cat,
        names="Category",
        values="Sales",
        hole=0.68,
        color_discrete_sequence=["#0D9488", "#3B82F6", "#F43F5E"]
    )
    fig_donut.update_layout(
        template="plotly_white",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#64748B"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text=f"<b>${rev_total/1000:,.0f}K</b><br><span style='font-size:10px; color:#64748B'>Total</span>", 
                          x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# Column 2: Team / Rep Performance Leaderboard
with c_mid:
    st.markdown("""<div class="analytics-card">
<div class="card-header-flex">
<h3 class="card-title">Team Performance</h3>
<span class="card-link">View All</span>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar" style="background:#0D9488;">AM</div>
<div class="rep-name">Alex Morgan</div>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width: 100%;"></div></div>
<div class="rep-val">$152,500</div>
<div class="rep-pct">102%</div>
</div>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar" style="background:#3B82F6;">JC</div>
<div class="rep-name">Jamie Carter</div>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width: 89%;"></div></div>
<div class="rep-val">$118,900</div>
<div class="rep-pct">89%</div>
</div>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar" style="background:#8B5CF6;">TB</div>
<div class="rep-name">Taylor Brooks</div>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width: 76%;"></div></div>
<div class="rep-val">$96,400</div>
<div class="rep-pct">76%</div>
</div>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar" style="background:#F59E0B;">JL</div>
<div class="rep-name">Jordan Lee</div>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width: 65%;"></div></div>
<div class="rep-val">$84,700</div>
<div class="rep-pct">65%</div>
</div>
</div>
<div class="rep-row" style="border-bottom:none;">
<div class="rep-profile">
<div class="rep-avatar" style="background:#F43F5E;">MR</div>
<div class="rep-name">Morgan Riley</div>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width: 54%;"></div></div>
<div class="rep-val">$72,300</div>
<div class="rep-pct">54%</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

# Column 3: Revenue Forecast
with c_right:
    # Build a clean predictive trend line
    df_ts = df_master.groupby("YearMonth")["Sales"].sum().reset_index()
    X = np.arange(len(df_ts)).reshape(-1, 1)
    y = df_ts["Sales"].values
    reg = LinearRegression().fit(X, y)
    
    # 4 future months
    future_X = np.arange(len(df_ts), len(df_ts) + 4).reshape(-1, 1)
    future_y = reg.predict(future_X)
    last_m = pd.Period(df_ts["YearMonth"].iloc[-1], freq="M")
    f_labels = [(last_m + i).strftime("%b") for i in range(1, 5)]

    fig_fc = go.Figure()
    # Historical recent points
    recent_labels = [pd.Period(m, freq="M").strftime("%b") for m in df_ts["YearMonth"].tail(6)]
    fig_fc.add_trace(go.Scatter(
        x=recent_labels,
        y=df_ts["Sales"].tail(6),
        name="Actual",
        mode="lines+markers",
        line=dict(color="#94A3B8", width=2)
    ))
    # Forecast line
    fig_fc.add_trace(go.Scatter(
        x=[recent_labels[-1]] + f_labels,
        y=[df_ts["Sales"].iloc[-1]] + list(future_y),
        name="Forecast",
        mode="lines+markers",
        line=dict(color="#0D9488", width=3, dash="dot"),
        marker=dict(size=7, color="#0D9488")
    ))
    fig_fc.update_layout(
        template="plotly_white",
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#64748B"),
        xaxis=dict(showgrid=False, linecolor="#E2E8F0"),
        yaxis=dict(gridcolor="#F1F5F9", showline=False),
        showlegend=False
    )

    pred_rev = future_y.sum()
    st.markdown(f"""<div class="analytics-card">
<div class="card-header-flex">
<h3 class="card-title">Revenue Forecast</h3>
<span class="card-link">Pipeline View</span>
</div>
<div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:10px;">
<div>
<span style="font-size:12px; color:#64748B; font-weight:600;">Predicted Forward Run-Rate</span>
<div style="font-size:24px; font-weight:800; color:#0F172A;">${pred_rev:,.0f}</div>
<span style="font-size:12px; font-weight:600; color:#10B981;">↑ +16.3% vs last quarter</span>
</div>
<div style="background:#E6FFFA; color:#0D9488; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:700;">
${future_y[0]/1000:,.0f}K Next Mo
</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_fc, use_container_width=True)

# ----------------- SECTION 3: DEEP-DIVE TABS (Regional, Products, Raw Data) -----------------
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

tab_reg, tab_prod, tab_table = st.tabs([
    "🌍 Regional Sales & City Breakdown",
    "📦 Product Portfolio & High Margin Stars",
    "📋 Searchable Order Book & CSV Export"
])

with tab_reg:
    col_re1, col_re2 = st.columns([1.2, 0.8])
    with col_re1:
        st.markdown("##### 📍 Regional Revenue & Profit Contribution")
        df_reg = filtered_df.groupby("Region").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        fig_r = go.Figure(data=[
            go.Bar(name="Revenue ($)", x=df_reg["Region"], y=df_reg["Sales"], marker_color="#0D9488"),
            go.Bar(name="Profit ($)", x=df_reg["Region"], y=df_reg["Profit"], marker_color="#3B82F6")
        ])
        fig_r.update_layout(
            template="plotly_white",
            barmode="group",
            height=320,
            font=dict(family="Plus Jakarta Sans", size=12, color="#64748B"),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#F1F5F9")
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with col_re2:
        st.markdown("##### 🏙️ Top 5 Performing Hubs")
        df_cities = filtered_df.groupby("City")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=True).tail(5)
        fig_c = px.bar(
            df_cities,
            x="Sales",
            y="City",
            orientation="h",
            color="Sales",
            color_continuous_scale=["#99F6E4", "#0D9488"]
        )
        fig_c.update_layout(
            template="plotly_white",
            height=320,
            font=dict(family="Plus Jakarta Sans", size=12, color="#64748B"),
            coloraxis_showscale=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_c, use_container_width=True)

with tab_prod:
    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        st.markdown("##### 🏆 Top 8 Best-Selling Products by Revenue")
        df_top_p = filtered_df.groupby("Product_Name")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(8)
        fig_tp = px.bar(
            df_top_p,
            x="Product_Name",
            y="Sales",
            color_discrete_sequence=["#0D9488"]
        )
        fig_tp.update_layout(
            template="plotly_white",
            height=340,
            xaxis_tickangle=-35,
            font=dict(family="Plus Jakarta Sans", size=11, color="#64748B"),
            yaxis=dict(gridcolor="#F1F5F9")
        )
        st.plotly_chart(fig_tp, use_container_width=True)

    with col_pr2:
        st.markdown("##### ⚖️ Sub-Category Margin Health")
        df_sub = filtered_df.groupby("Sub_Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        df_sub["Margin"] = (df_sub["Profit"] / df_sub["Sales"]) * 100
        df_sub = df_sub.sort_values(by="Margin", ascending=True)
        fig_sub = px.bar(
            df_sub,
            x="Margin",
            y="Sub_Category",
            orientation="h",
            color="Margin",
            color_continuous_scale=["#FDA4AF", "#10B981"]
        )
        fig_sub.update_layout(
            template="plotly_white",
            height=340,
            font=dict(family="Plus Jakarta Sans", size=11, color="#64748B"),
            coloraxis_showscale=False,
            xaxis_title="Margin (%)"
        )
        st.plotly_chart(fig_sub, use_container_width=True)

with tab_table:
    st.markdown("##### 🔍 Search & Filter Orders")
    search = st.text_input("Quick search across Customer, Order ID, or Product", "")
    t_df = filtered_df.copy()
    if search:
        t_df = t_df[
            t_df["Customer_Name"].str.contains(search, case=False, na=False) |
            t_df["Product_Name"].str.contains(search, case=False, na=False) |
            t_df["Order_ID"].str.contains(search, case=False, na=False)
        ]

    cols_show = ["Order_ID", "Order_Date", "Customer_Name", "Region", "Category", "Product_Name", "Quantity", "Sales", "Profit", "Rating"]
    st.dataframe(
        t_df[cols_show].style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}"
        }),
        use_container_width=True,
        height=320
    )

    csv_data = t_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Orders CSV",
        data=csv_data,
        file_name=f"sales_data_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
