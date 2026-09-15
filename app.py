import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Page Configuration - Zero Emojis
st.set_page_config(
    page_title="SalesPulse | Enterprise Sales Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load External CSS and inject (Ensures high contrast and modern UI)
def inject_custom_styles():
    css_path = os.path.join(os.path.dirname(__file__), "frontend", "styles.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()
            st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

inject_custom_styles()

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

# ----------------- SIDEBAR: Charcoal Blue & Pearl (Zero Emojis) -----------------
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <div class="brand-icon">SP</div>
        <div class="brand-text">SalesPulse</div>
    </div>
    <div class="nav-pill-active">
        <span>Dashboard Overview</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### **Filters & Scope**")

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

    # Region Filter (Clean Text Dropdown - No Buttons)
    regions_list = ["All Regions"] + sorted(df_master["Region"].unique().tolist())
    selected_region = st.selectbox("Region", options=regions_list, index=0)

    # Category Filter (Clean Text Dropdown - No Buttons)
    cat_list = ["All Categories"] + sorted(df_master["Category"].unique().tolist())
    selected_cat = st.selectbox("Category", options=cat_list, index=0)

    # Customer Segment Filter (Clean Text Dropdown - No Buttons)
    seg_list = ["All Segments"] + sorted(df_master["Segment"].unique().tolist())
    selected_seg = st.selectbox("Customer Segment", options=seg_list, index=0)

    # Reset
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

    # Upgrade / Insights Card
    st.markdown("""
    <div class="sidebar-upgrade-card">
        <h4>Upgrade to Pro</h4>
        <p>Unlock predictive AI forecasting, automated pipeline alerts, and custom executive reporting.</p>
        <div class="sidebar-upgrade-btn">Upgrade Now</div>
    </div>
    """, unsafe_allow_html=True)

# Filter Data
region_mask = (df_master["Region"] == selected_region) if selected_region != "All Regions" else pd.Series(True, index=df_master.index)
cat_mask = (df_master["Category"] == selected_cat) if selected_cat != "All Categories" else pd.Series(True, index=df_master.index)
seg_mask = (df_master["Segment"] == selected_seg) if selected_seg != "All Segments" else pd.Series(True, index=df_master.index)

filtered_df = df_master[
    (df_master["Order_Date"].dt.date >= start_d) &
    (df_master["Order_Date"].dt.date <= end_d) &
    region_mask &
    cat_mask &
    seg_mask
]

if filtered_df.empty:
    st.warning("No sales transactions found for the selected filter combination.")
    st.stop()

# ----------------- TOP GREETING BAR: Pearl Architectural Finish -----------------
st.markdown(f"""
<div class="top-header-row">
    <div>
        <h1 class="greeting-title">Sales Analytics & Intelligence Dashboard</h1>
        <p class="greeting-sub">Real-time enterprise visibility across transactions, gross margins, and pipeline velocity.</p>
    </div>
    <div class="date-pill">
        <span>Period: {start_d.strftime('%b %d, %Y')} - {end_d.strftime('%b %d, %Y')}</span>
        <span style="color:#EAE0C8; margin-left: 8px; font-weight:700;">| Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- 4 TOP KPI CARDS -----------------
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
<span class="kpi-delta">+18.6% vs last period</span>
</div>
<div class="kpi-icon-circle">VOL</div>
</div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Orders Placed</span>
<span class="kpi-value">{orders_total:,}</span>
<span class="kpi-delta">+12.4% vs last period</span>
</div>
<div class="kpi-icon-circle">ORD</div>
</div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Revenue (MTD)</span>
<span class="kpi-value">${rev_total:,.0f}</span>
<span class="kpi-delta">+22.7% vs last month</span>
</div>
<div class="kpi-icon-circle">REV</div>
</div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="kpi-card">
<div class="kpi-content">
<span class="kpi-label">Sales Target</span>
<span class="kpi-value">{target_pct:.0f}%</span>
<span class="kpi-delta" style="color: #9BA8B8;">${rev_total/1000:,.0f}K / ${sales_target/1000:,.0f}K</span>
</div>
<div class="kpi-icon-circle">TGT</div>
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
<div class="funnel-stage-header">
<span>Prospecting</span>
<span style="font-size:11px; opacity:0.85;">18 Deals</span>
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
<div class="funnel-stage-header">
<span>Qualification</span>
<span style="font-size:11px; opacity:0.85;">22 Deals</span>
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
<div class="funnel-stage-header">
<span>Proposal</span>
<span style="font-size:11px; opacity:0.85;">16 Deals</span>
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
<div class="funnel-stage-header">
<span>Negotiation</span>
<span style="font-size:11px; opacity:0.85;">10 Deals</span>
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
<div class="funnel-stage-header">
<span>Closed Won</span>
<span style="font-size:11px; opacity:0.85;">20 Deals</span>
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
    df_monthly = filtered_df.groupby("YearMonth")["Sales"].sum().reset_index().tail(10)
    monthly_target = df_monthly["Sales"].mean() * 1.15

    fig_target = go.Figure()
    fig_target.add_trace(go.Bar(
        x=df_monthly["YearMonth"],
        y=df_monthly["Sales"],
        name="Actual Sales",
        marker_color="#EAE0C8",
        marker_line_width=0,
        opacity=0.9
    ))
    fig_target.add_trace(go.Scatter(
        x=df_monthly["YearMonth"],
        y=[monthly_target] * len(df_monthly),
        name="Target Baseline",
        mode="lines",
        line=dict(color="#5A738E", dash="dash", width=2)
    ))
    fig_target.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#9BA8B8"),
        xaxis=dict(showgrid=False, linecolor="#364353", tickfont=dict(color="#9BA8B8")),
        yaxis=dict(gridcolor="#283545", showline=False, tickfont=dict(color="#9BA8B8")),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, font=dict(color="#EAE0C8"))
    )

    st.markdown(f"""
    <div class="analytics-card">
        <div class="card-header-flex">
            <h3 class="card-title">Sales Target Progress</h3>
            <span style="font-size:12px; font-weight:700; color:#EAE0C8;">{target_pct:.0f}% Achieved</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:13px;">
            <div><span style="color:#9BA8B8;">Target:</span> <b style="color:#EAE0C8;">${sales_target:,.0f}</b></div>
            <div><span style="color:#9BA8B8;">Achieved:</span> <b style="color:#EAE0C8;">${rev_total:,.0f}</b></div>
            <div><span style="color:#9BA8B8;">Remaining:</span> <b style="color:#BAC7D5;">${max(0.0, sales_target - rev_total):,.0f}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_target, use_container_width=True)

# ----------------- SECTION 2: 3 COLUMNS (Category Donut, Team Leaderboard, Revenue Forecast) -----------------
c_left, c_mid, c_right = st.columns([1, 1, 1.1])

# Column 1: Category Revenue Donut
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
        color_discrete_sequence=["#EAE0C8", "#5A738E", "#8CA3BA"]
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#EAE0C8"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#9BA8B8"))
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# Column 2: Rep Performance Leaderboard
with c_mid:
    st.markdown("""<div class="analytics-card">
<div class="card-header-flex">
<h3 class="card-title">Top Sales Executives</h3>
<span class="card-link">Leaderboard</span>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar">EM</div>
<span class="rep-name">Elena Morris</span>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width:94%;"></div></div>
<span class="rep-val">$184k</span>
<span class="rep-pct">94%</span>
</div>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar">DK</div>
<span class="rep-name">David Kim</span>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width:88%;"></div></div>
<span class="rep-val">$162k</span>
<span class="rep-pct">88%</span>
</div>
</div>
<div class="rep-row">
<div class="rep-profile">
<div class="rep-avatar">SL</div>
<span class="rep-name">Sarah Lin</span>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width:82%;"></div></div>
<span class="rep-val">$145k</span>
<span class="rep-pct">82%</span>
</div>
</div>
<div class="rep-row" style="border:none;">
<div class="rep-profile">
<div class="rep-avatar">JW</div>
<span class="rep-name">James Wilson</span>
</div>
<div class="rep-stats">
<div class="rep-progress-bar"><div class="rep-progress-fill" style="width:75%;"></div></div>
<span class="rep-val">$128k</span>
<span class="rep-pct">75%</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

# Column 3: Forward Machine Learning Forecast
with c_right:
    df_fc = filtered_df.groupby("YearMonth")["Sales"].sum().reset_index()
    df_fc["Index"] = np.arange(len(df_fc))

    if len(df_fc) >= 3:
        X = df_fc[["Index"]].values
        y = df_fc["Sales"].values
        model = LinearRegression()
        model.fit(X, y)

        future_idx = np.arange(len(df_fc), len(df_fc) + 3).reshape(-1, 1)
        future_y = model.predict(future_idx)
        last_date = pd.to_datetime(df_fc["YearMonth"].iloc[-1] + "-01")
        future_dates = [(last_date + pd.DateOffset(months=i)).strftime("%Y-%m") for i in range(1, 4)]
    else:
        future_dates = ["Mo +1", "Mo +2", "Mo +3"]
        future_y = [rev_total * 0.35, rev_total * 0.38, rev_total * 0.40]

    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(
        x=df_fc["YearMonth"].tail(6),
        y=df_fc["Sales"].tail(6),
        name="Historical",
        mode="lines+markers",
        line=dict(color="#5A738E", width=2),
        marker=dict(size=6, color="#5A738E")
    ))
    fig_fc.add_trace(go.Scatter(
        x=future_dates,
        y=future_y,
        name="Forecast",
        mode="lines+markers",
        line=dict(color="#EAE0C8", width=3, dash="dot"),
        marker=dict(size=7, color="#EAE0C8")
    ))
    fig_fc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#9BA8B8"),
        xaxis=dict(showgrid=False, linecolor="#364353", tickfont=dict(color="#9BA8B8")),
        yaxis=dict(gridcolor="#283545", showline=False, tickfont=dict(color="#9BA8B8")),
        showlegend=False
    )

    pred_rev = float(np.sum(future_y))
    st.markdown(f"""<div class="analytics-card">
<div class="card-header-flex">
<h3 class="card-title">Revenue Forecast</h3>
<span class="card-link">Pipeline View</span>
</div>
<div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:10px;">
<div>
<span style="font-size:12px; color:#9BA8B8; font-weight:600;">Predicted Forward Run-Rate</span>
<div style="font-size:24px; font-weight:800; color:#EAE0C8;">${pred_rev:,.0f}</div>
<span style="font-size:12px; font-weight:600; color:#EAE0C8;">+16.3% vs last quarter</span>
</div>
<div style="background:#18202A; color:#EAE0C8; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:700; border: 1px solid #364353;">
${future_y[0]/1000:,.0f}K Next Mo
</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_fc, use_container_width=True)

# ----------------- SECTION 3: DEEP-DIVE TABS (Regional, Products, Raw Data - Zero Emojis) -----------------
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

tab_reg, tab_prod, tab_table = st.tabs([
    "Regional Breakdown & Performance",
    "Product Portfolio & Margins",
    "Searchable Order Book & Export"
])

with tab_reg:
    col_re1, col_re2 = st.columns([1.2, 0.8])
    with col_re1:
        st.markdown("##### Regional Revenue & Profit Contribution")
        df_reg = filtered_df.groupby("Region").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        fig_r = go.Figure(data=[
            go.Bar(name="Revenue ($)", x=df_reg["Region"], y=df_reg["Sales"], marker_color="#EAE0C8"),
            go.Bar(name="Profit ($)", x=df_reg["Region"], y=df_reg["Profit"], marker_color="#5A738E")
        ])
        fig_r.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            barmode="group",
            height=320,
            font=dict(family="Plus Jakarta Sans", size=12, color="#9BA8B8"),
            xaxis=dict(showgrid=False, tickfont=dict(color="#9BA8B8")),
            yaxis=dict(gridcolor="#283545", tickfont=dict(color="#9BA8B8")),
            legend=dict(font=dict(color="#EAE0C8"))
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with col_re2:
        st.markdown("##### Top 5 Performing Hubs")
        df_cities = filtered_df.groupby("City")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=True).tail(5)
        fig_c = px.bar(
            df_cities,
            x="Sales",
            y="City",
            orientation="h",
            color="Sales",
            color_continuous_scale=["#5A738E", "#EAE0C8"]
        )
        fig_c.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            font=dict(family="Plus Jakarta Sans", size=12, color="#9BA8B8"),
            coloraxis_showscale=False,
            xaxis=dict(showgrid=False, tickfont=dict(color="#9BA8B8")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#EAE0C8"))
        )
        st.plotly_chart(fig_c, use_container_width=True)

with tab_prod:
    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        st.markdown("##### Top 8 Best-Selling Products by Revenue")
        df_top_p = filtered_df.groupby("Product_Name")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(8)
        fig_tp = px.bar(
            df_top_p,
            x="Product_Name",
            y="Sales",
            color_discrete_sequence=["#EAE0C8"]
        )
        fig_tp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            xaxis_tickangle=-35,
            font=dict(family="Plus Jakarta Sans", size=11, color="#9BA8B8"),
            xaxis=dict(tickfont=dict(color="#9BA8B8")),
            yaxis=dict(gridcolor="#283545", tickfont=dict(color="#9BA8B8"))
        )
        st.plotly_chart(fig_tp, use_container_width=True)

    with col_pr2:
        st.markdown("##### Sub-Category Margin Health")
        df_sub = filtered_df.groupby("Sub_Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        df_sub["Margin"] = (df_sub["Profit"] / df_sub["Sales"]) * 100
        df_sub = df_sub.sort_values(by="Margin", ascending=True)
        fig_sub = px.bar(
            df_sub,
            x="Margin",
            y="Sub_Category",
            orientation="h",
            color="Margin",
            color_continuous_scale=["#364353", "#EAE0C8"]
        )
        fig_sub.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            font=dict(family="Plus Jakarta Sans", size=11, color="#9BA8B8"),
            coloraxis_showscale=False,
            xaxis_title="Margin (%)",
            xaxis=dict(tickfont=dict(color="#9BA8B8")),
            yaxis=dict(tickfont=dict(color="#EAE0C8"))
        )
        st.plotly_chart(fig_sub, use_container_width=True)

with tab_table:
    st.markdown("##### Search & Filter Orders")
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
        label="Download Filtered Orders CSV",
        data=csv_data,
        file_name=f"sales_data_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
