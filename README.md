# 💰 Personal Finance Dashboard with Streamlit

This repository hosts an interactive application developed with **Streamlit** for expert personal finance analysis. Its objective is to transform raw data from bank transactions and account balances into **Key Performance Indicators (KPIs)** and actionable visualizations, enabling informed financial decision-making.

## 🚀 Key Dashboard Features

The dashboard design is based on visual hierarchy and usability, providing essential information at a glance:

### 1. Key Performance Indicators (KPIs)

Header section with critical metrics for financial health:

* **Current Total Balance:** Total liquidity in a single number.

* **Income:** Income for the selected period. This indicator shows fixed income, excluding extras.

* **Expenses:** Expenses for the selected period.

* **Savings/Spending Rate:** The percentage of income being saved or overspent.

### 2. Trend Analysis

* **Temporal Evolution of Income vs. Expenses:** Line chart comparing cash flow dynamics over time.

* **Expense Distribution by Category:** Pie/donut chart to visualize where spending is concentrated (Housing, Leisure, Food, etc.).

### 3. Account Monitoring

* **Capital Distribution:** Visualization of the total balance distribution across different bank accounts.

* **Account Detail:** Table showing Initial Balance, Final Balance, and Net Movement per account.

### 4. Interaction Tools (Sidebar)

All charts are dynamic and update with the filters available in the sidebar:

* **Date Range Selector:** Main filter to select the analysis period.

## 📊 Layout Structure (Streamlit Design)

The design utilizes Streamlit functions for optimal presentation:

| **Section** | **Streamlit Components** | **Purpose** |
| :--- | :--- | :--- |
| **Filter Panel** | `st.sidebar` (Selectors, Date Range) | Global Control and Filters |
| **Header** | `st.columns(4)` with `st.metric` | Immediate Summary and Critical KPIs |
| **Main Area 1** | Line Chart (Full Width) | Cash Flow Trend Analysis |
| **Main Area 2** | `st.columns(2)` (Pie Chart + Balance Table) | Detailed Expense and Liquidity Breakdown |

## 🛠️ Data Requirements

The application is designed to consume data from two sheets within a single Excel file (or two CSV files):

1. **Movements Sheet (`movimientos`)**:

   * `fecha` (Date)

   * `importe` (Float)

   * `categoria del gasto` (String)

   * `cuenta` (String)

2. **Accounts Sheet (`cuentas`)**:

   * `cuenta` (String)

   * `saldo inicial` (Float)

   * `saldo final` (Float - Calculated or from data)

## 💻 Installation and Usage

1. **Clone the repository:**

   ```bash
   git clone [YOUR_REPO_URL]
   cd [repo_name]
