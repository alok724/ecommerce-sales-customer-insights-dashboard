# 📊 E-Commerce Sales & Customer Insights Dashboard

Hey there! 👋 This is an executive-level Business Intelligence project I built using the UCI Online Retail dataset to uncover deep insights into revenue performance, operational bottlenecks, cancellation risks, and high-value customer segmentation.

---

## 🚀 Project Overview
I created this project to bridge the gap between raw data engineering and executive decision-making. It transforms messy transaction logs into a polished, 4-page interactive Power BI dashboard that tackles real-world challenges like data governance, revenue leakage, and customer purchasing patterns.

---

## 📑 Dashboard Breakdown & Visuals

### Page 1: Executive Overview
* **Net Line Value:** £9.73M
* **Gross Positive Sales:** £10.64M
* **Qualifying Invoices:** 19,960
* *What's inside:* High-level performance tracking, monthly sales trends, hourly distribution, and top-performing countries/products.

![Executive Overview](assets/page1_executive_overview.png)

---

### Page 2: Operational Deep Dive
* **Net Quantity Across Rows:** 5.16M
* **Total Distinct Invoices:** 25,900
* *What's inside:* Day-of-week sales patterns (taking into account warehouse Saturday closures!), product quantity analysis, and order volume trends.

![Operational Deep Dive](assets/page2_operational_deep_dive.png)

---

### Page 3: Cancellations & Risk Analysis
* **Cancellation Invoices:** 3,836 (resulting in a 14.81% cancellation rate)
* **Gross-to-Net Sales Difference:** £916.1K
* *What's inside:* Hourly cancellation peaks, country-level risk distribution, and tracking financial gaps.

![Cancellations & Risk](assets/page3_cancellations_risk.png)

---

### Page 4: Customer Insights
* **Identified Customers:** 4.4K customers driving 83.5% (£8.89M) of total positive sales.
* *What's inside:* Pinpointing top 10 customers, scatter-plotting customer spending versus purchase frequency, and comparing registered users against guest checkouts.

![Customer Insights](assets/page4_customer_insights.png)

---

## 🛠️ Tech Stack & Tools I Used
- **Python (Pandas, NumPy):** Handled data ingestion, cleaned missing values, filtered anomalous rows, and formatted date-time stamps.
- **MySQL:** Managed relational data, ran exploratory queries, and validated core financial metrics via custom scripts (`ecommerce_analysis.sql`).
- **Power BI Desktop:** Built data models, wrote custom DAX measures, and structured executive-friendly layouts.
- **Git & GitHub:** Maintained clean version control and professional documentation.

---

## 📂 Repository File Structure
```text
ecommerce-sales-customer-insights-dashboard/
├── assets/                             # Dashboard screenshots for README
│   ├── page1_executive_overview.png
│   ├── page2_operational_deep_dive.png
│   ├── page3_cancellations_risk.png
│   └── page4_customer_insights.png
├── powerbi/
│   ├── Ecommerce_Sales_Dashboard.pbix  # Main interactive Power BI report file
│   └── Ecommerce_Sales_Dashboard.pdf   # High-resolution 4-page executive PDF export
├── sql/
│   └── ecommerce_analysis.sql          # MySQL queries and financial validation script
├── main.py                             # Python data cleaning and processing pipeline
├── prepare_mysql_csv.py                # Helper script for database preparation
└── README.md                           # Project documentation