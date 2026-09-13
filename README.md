# 📊 Enterprise Sales Dashboard & Business Intelligence Project

A modern, interactive Python-based **Sales Analytics & Intelligence Dashboard** built with **Streamlit**, **Plotly**, **Pandas**, and **Scikit-Learn**. 

Designed for Data Analyst and Data Science portfolios, business reporting, and executive decision-making.

---

## 🌟 Key Features

1. **Executive KPI Cards**:
   - Total Gross Revenue ($)
   - Net Profit & Overall Profit Margin (%)
   - Total Orders Placed & Units Sold
   - Average Order Value (AOV)
   - Customer CSAT Rating

2. **Dynamic Sidebar Filter Engine**:
   - Date range selector (2024 to 2026)
   - Multi-select Regions (North, South, East, West, Central)
   - Multi-select Product Categories (Technology, Furniture, Office Supplies)
   - Customer Segments (Consumer, Corporate, Home Office)
   - Payment Methods (Credit Card, Debit Card, UPI, Net Banking, COD)
   - One-click **Reset All Filters** button

3. **6 Analytics Deep-Dive Modules (Tabs)**:
   - 📈 **Revenue & Trends**: Monthly sales vs net profit combined chart with a 3-month rolling moving average, day-of-week sales volume, and shipping mode split.
   - 🌍 **Geographical Performance**: Revenue & profit comparisons across regions, top 10 revenue-generating cities, and a category-wise regional margin heatmap.
   - 📦 **Product & Category Analytics**: Category market share donut chart, sub-category performance rankings, and top 10 best-selling products.
   - 👥 **Customer & Discounts**: Segment-wise revenue, preferred payment distribution, and discount vs profit margin erosion scatter analysis.
   - 🔮 **Predictive Sales Forecasting**: Machine learning Linear Trend model predicting upcoming 4-month revenues with confidence intervals and annualized growth momentum.
   - 📋 **Data Explorer & Export**: Searchable data table with instant 1-click CSV download.

---

## 🚀 How to Run

### Method 1: 1-Click Launch (Windows)
Double-click the [`run_dashboard.bat`](./run_dashboard.bat) file in this folder.

### Method 2: Terminal / Command Prompt
1. Open terminal inside this folder:
```bash
streamlit run app.py
```
2. The dashboard will automatically open in your default web browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
Sales Dashboard Analytics Project/
├── app.py                  # Main Streamlit Dashboard application
├── generate_data.py        # Realistic sales dataset generation engine
├── run_dashboard.bat       # Double-click Windows launcher
├── README.md               # Project documentation & portfolio guide
├── .streamlit/
│   └── config.toml         # Custom dark theme and server settings
└── data/
    └── sales_data.csv      # 1,800+ realistic retail transaction records
```

---

## 💡 How to Describe this Project in Interviews / Resume

> **"Developed an end-to-end Enterprise Sales Intelligence Dashboard in Python using Streamlit, Plotly, and Scikit-Learn. Engineered a multi-factor transactional dataset with 1,800+ records, built interactive multi-dimensional filter controls, visual analytics for regional and product margin health, and implemented a linear regression forecasting pipeline to project forward 4-month sales."**
