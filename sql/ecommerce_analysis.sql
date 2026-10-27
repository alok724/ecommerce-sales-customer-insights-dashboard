-- =====================================================================
-- PROJECT: E-COMMERCE SALES & CUSTOMER INSIGHTS DASHBOARD
-- DATABASE: ecommerce_analysis
-- TABLE: online_retail_mysql
-- =====================================================================

-- create database ecommerce_analysis;
USE ecommerce_analysis;

-- CREATE TABLE IF NOT EXISTS online_retail_mysql (
--     InvoiceNo VARCHAR(20) NULL,
--     StockCode VARCHAR(20) NULL,
--     Description VARCHAR(255) NULL,
--     Quantity INT NULL,
--     InvoiceDate DATETIME NULL,
--     UnitPrice DECIMAL(10,2) NULL,
--     CustomerID INT NULL,
--     Country VARCHAR(100) NULL,
--     is_cancellation_invoice TINYINT(1) NULL,
--     is_negative_quantity TINYINT(1) NULL,
--     is_zero_price TINYINT(1) NULL,
--     has_missing_description TINYINT(1) NULL,
--     has_missing_customer_id TINYINT(1) NULL,
--     line_value DECIMAL(12,2) NULL,
--     year INT NULL,
--     month INT NULL,
--     month_name VARCHAR(15) NULL,
--     day_of_week VARCHAR(15) NULL,
--     hour INT NULL,
--     is_weekend TINYINT(1) NULL,
--     is_cancellation TINYINT(1) NULL,
--     is_negative_price TINYINT(1) NULL,
--     has_customer_id TINYINT(1) NULL,
--     positive_sales_value DECIMAL(12,2) NULL,
--     invoice_prefix_c TINYINT(1) NULL
-- );
-- =====================================================================

-- PHASE 1: DATA VALIDATION & QUALITY AUDIT
-- =====================================================================

-- Query 1: Verify Table Structure & Row Count
-- What it does: Checks all tables in the database and counts total imported rows.
-- Why we use it: To confirm all 536,641 cleaned rows from Python loaded without data loss.
SHOW TABLES;

SELECT 
    COUNT(*) AS total_rows
FROM
    online_retail_mysql;


-- Query 2: Verify Column Count & Schema Definitions
-- What it does: Counts total columns and displays column data types.
-- Why we use it: To ensure all 25 columns exist with proper types (VARCHAR, DATETIME, DECIMAL, TINYINT).
SELECT 
    COUNT(*) AS total_columns
FROM
    INFORMATION_SCHEMA.COLUMNS
WHERE
    TABLE_SCHEMA = 'ecommerce_analysis'
        AND TABLE_NAME = 'online_retail_mysql';

DESCRIBE online_retail_mysql;


-- Query 3: Sample Data Preview
-- What it does: Displays the first 10 rows of the dataset.
-- Why we use it: To visually verify that dates, decimals, text descriptions, and binary flags (0/1) are aligned properly.
SELECT 
    *
FROM
    online_retail_mysql
LIMIT 10;


-- Query 4: Audit Missing Values & Transaction Anomalies
-- What it does: Counts missing CustomerIDs, missing Descriptions, cancellations, negative quantities, and zero/negative prices.
-- Why we use it: Uses our pre-built 0/1 binary flags with simple SUM().
SELECT 
    COUNT(*) AS total_rows,
    SUM(has_missing_customer_id) AS missing_customer_ids,
    SUM(has_missing_description) AS missing_descriptions,
    SUM(is_negative_quantity) AS negative_quantity_rows,
    SUM(is_zero_price) AS zero_price_rows,
    SUM(is_negative_price) AS negative_price_rows,
    SUM(is_cancellation_invoice) AS cancellation_invoice_rows
FROM
    online_retail_mysql;


-- Query 5: Validate Engineered Binary Flags (All 10 Flags for Counts & Invalid Values)
-- What it does: Sums up all 10 binary flags and checks that values are strictly 0 or 1 with no NULLs.
-- Why we use it: To guarantee data integrity of our engineered Python features before analysis.
SELECT 
    SUM(is_cancellation_invoice) AS flag_cancellation_inv,
    SUM(is_negative_quantity) AS flag_neg_qty,
    SUM(is_zero_price) AS flag_zero_price,
    SUM(has_missing_description) AS flag_missing_desc,
    SUM(has_missing_customer_id) AS flag_missing_cust,
    SUM(is_weekend) AS flag_weekend,
    SUM(is_cancellation) AS flag_cancellation,
    SUM(is_negative_price) AS flag_neg_price,
    SUM(has_customer_id) AS flag_has_cust,
    SUM(invoice_prefix_c) AS flag_prefix_c,
    SUM(is_cancellation_invoice IS NULL
        OR is_cancellation_invoice NOT IN (0 , 1)) AS invalid_cancellation_invoice_flags,
    SUM(is_negative_quantity IS NULL
        OR is_negative_quantity NOT IN (0 , 1)) AS invalid_negative_quantity_flags,
    SUM(is_zero_price IS NULL
        OR is_zero_price NOT IN (0 , 1)) AS invalid_zero_price_flags,
    SUM(has_missing_description IS NULL
        OR has_missing_description NOT IN (0 , 1)) AS invalid_missing_description_flags,
    SUM(has_missing_customer_id IS NULL
        OR has_missing_customer_id NOT IN (0 , 1)) AS invalid_missing_customer_flags,
    SUM(is_weekend IS NULL
        OR is_weekend NOT IN (0 , 1)) AS invalid_weekend_flags,
    SUM(is_cancellation IS NULL
        OR is_cancellation NOT IN (0 , 1)) AS invalid_cancellation_flags,
    SUM(is_negative_price IS NULL
        OR is_negative_price NOT IN (0 , 1)) AS invalid_negative_price_flags,
    SUM(has_customer_id IS NULL
        OR has_customer_id NOT IN (0 , 1)) AS invalid_customer_id_flags,
    SUM(invoice_prefix_c IS NULL
        OR invoice_prefix_c NOT IN (0 , 1)) AS invalid_prefix_c_flags
FROM
    online_retail_mysql;


-- Query 5B: Flag Consistency Checks against Underlying Raw Conditions
-- What it does: Cross-verifies all 10 binary flags against their source columns using null-safe equality (<=>).
-- Why we use it: To ensure Python feature engineering rules match SQL evaluation rules with zero mismatches.
SELECT 
    SUM(NOT (has_customer_id <=> (CustomerID IS NOT NULL))) AS customer_flag_mismatches,
    SUM(NOT (has_missing_customer_id <=> (CustomerID IS NULL))) AS missing_customer_flag_mismatches,
    SUM(NOT (has_missing_description <=> (Description IS NULL))) AS missing_description_flag_mismatches,
    SUM(NOT (is_negative_quantity <=> (Quantity < 0))) AS negative_quantity_flag_mismatches,
    SUM(NOT (is_zero_price <=> (UnitPrice = 0))) AS zero_price_flag_mismatches,
    SUM(NOT (is_negative_price <=> (UnitPrice < 0))) AS negative_price_flag_mismatches,
    SUM(NOT (is_cancellation_invoice <=> (InvoiceNo LIKE 'C%'))) AS cancellation_invoice_flag_mismatches,
    SUM(NOT (is_cancellation <=> (InvoiceNo LIKE 'C%'))) AS cancellation_flag_mismatches,
    SUM(NOT (is_weekend <=> (day_of_week IN ('Saturday' , 'Sunday')))) AS weekend_flag_mismatches,
    SUM(NOT (invoice_prefix_c <=> (InvoiceNo LIKE 'C%'))) AS invoice_prefix_c_flag_mismatches
FROM
    online_retail_mysql;


-- =====================================================================
-- PHASE 2: OVERALL BUSINESS KPIs & SALES PERFORMANCE
-- =====================================================================

SELECT 
    COUNT(*) AS total_transaction_rows,
    COUNT(DISTINCT InvoiceNo) AS unique_invoices,
    COUNT(DISTINCT CustomerID) AS unique_identified_customers,
    COUNT(DISTINCT StockCode) AS unique_stock_codes,
    SUM(Quantity) AS net_quantity_across_rows,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value_total,
    ROUND(SUM(line_value), 2) AS net_line_value
FROM
    online_retail_mysql;


-- Query 7: Monthly Sales Trend & Order Volume
-- What it does: Groups positive sales, net line value, and order counts by year and month.
-- Why we use it: To track seasonal sales growth and identify peak shopping months (like the November holiday spike).
SELECT 
    year,
    month,
    month_name,
    COUNT(DISTINCT InvoiceNo) AS total_invoices,
    SUM(Quantity) AS total_quantity,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value,
    ROUND(SUM(line_value), 2) AS net_line_value
FROM
    online_retail_mysql
GROUP BY year , month , month_name
ORDER BY year , month;


-- Query 8: Month-over-Month (MoM) Revenue Growth (Using CTE & Window Function)
-- What it does: Compares each month's net line value with the previous month's value using LAG().
-- Why we use it: Demonstrating CTEs and Window Functions to measure business momentum safely with NULLIF.
WITH monthly_sales AS (
    SELECT 
        year,
        month,
        month_name,
        ROUND(SUM(line_value), 2) AS net_line_value
    FROM
        online_retail_mysql
    GROUP BY year , month , month_name
),
monthly_comparison AS (
    SELECT 
        year,
        month,
        month_name,
        net_line_value,
        LAG(net_line_value) OVER (ORDER BY year, month) AS prev_month_net_line_value
    FROM
        monthly_sales
)
SELECT 
    year,
    month,
    month_name,
    net_line_value,
    prev_month_net_line_value,
    ROUND(
        100.0 * (net_line_value - prev_month_net_line_value)
        / NULLIF(prev_month_net_line_value, 0),
        2
    ) AS mom_growth_percentage
FROM
    monthly_comparison
ORDER BY year , month;


-- =====================================================================
-- PHASE 3: GEOGRAPHIC & COUNTRY PERFORMANCE
-- =====================================================================

SELECT 
    Country,
    COUNT(DISTINCT InvoiceNo) AS invoice_count,
    COUNT(DISTINCT CustomerID) AS identified_customers,
    SUM(Quantity) AS net_quantity_across_rows,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value,
    ROUND(SUM(line_value), 2) AS net_line_value
FROM
    online_retail_mysql
GROUP BY Country
ORDER BY positive_sales_value DESC
LIMIT 15;


-- =====================================================================
-- PHASE 4: PRODUCT PERFORMANCE INSIGHTS
-- =====================================================================

-- Query 10: Top 15 Revenue-Generating Products (With RANK Window Function)
-- What it does: Finds the top products by positive sales value and ranks them using RANK().
-- Why we use it: Identifies star products driving the highest cash flow for the business.
SELECT 
    StockCode,
    Description,
    COUNT(DISTINCT InvoiceNo) AS invoice_count,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value,
    RANK() OVER (ORDER BY SUM(positive_sales_value) DESC) AS revenue_rank
FROM
    online_retail_mysql
WHERE Quantity > 0 
  AND Description IS NOT NULL 
  AND is_cancellation = 0
GROUP BY StockCode , Description
ORDER BY positive_sales_value DESC
LIMIT 15;


-- Query 11: Top 15 Best-Selling Products by Quantity Sold
-- What it does: Ranks products by highest unit volume sold (excluding negative return quantities).
-- Why we use it: Helps inventory teams distinguish high-volume everyday items from high-price items.
SELECT 
    StockCode,
    Description,
    SUM(Quantity) AS total_units_sold,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value,
    COUNT(DISTINCT InvoiceNo) AS invoice_count
FROM
    online_retail_mysql
WHERE
    Quantity > 0 AND Description IS NOT NULL
        AND is_cancellation = 0
GROUP BY StockCode , Description
ORDER BY total_units_sold DESC
LIMIT 15;


-- =====================================================================
-- PHASE 5: CUSTOMER INSIGHTS & SEGMENTATION
-- =====================================================================

SELECT 
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS non_cancellation_orders,
    SUM(Quantity) AS total_items_across_rows,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_spend,
    ROUND(SUM(line_value), 2) AS net_line_value,
    MIN(InvoiceDate) AS first_transaction_date,
    MAX(InvoiceDate) AS last_transaction_date
FROM
    online_retail_mysql
WHERE
    CustomerID IS NOT NULL
        AND is_cancellation = 0
GROUP BY CustomerID
ORDER BY positive_sales_spend DESC
LIMIT 15;


-- Query 13: Identified vs. Unidentified (Missing CustomerID) Revenue Split
-- What it does: Compares sales coming from known CustomerIDs versus unidentified records.
-- Why we use it: Crucial business insight showing why we did not delete the 135,037 rows missing a CustomerID.
SELECT 
    CASE
        WHEN CustomerID IS NOT NULL THEN 'Identified Customer'
        ELSE 'Unidentified Customer'
    END AS customer_type,
    COUNT(*) AS transaction_rows,
    COUNT(DISTINCT InvoiceNo) AS total_invoices,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value,
    ROUND(SUM(line_value), 2) AS net_line_value
FROM
    online_retail_mysql
GROUP BY CASE
    WHEN CustomerID IS NOT NULL THEN 'Identified Customer'
    ELSE 'Unidentified Customer'
END;


-- Query 14: Customer Purchase Frequency & Spending Summary
-- What it does: Summarizes each customer's last purchase date, total orders, and total spend.
-- Why we use it: Simple customer summary to identify repeat buyers and high-value accounts.
SELECT 
    CustomerID,
    MAX(InvoiceDate) AS last_purchase_date,
    COUNT(DISTINCT InvoiceNo) AS frequency_orders,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_spend
FROM
    online_retail_mysql
WHERE
    CustomerID IS NOT NULL
        AND is_cancellation = 0
        AND positive_sales_value > 0
GROUP BY CustomerID
ORDER BY positive_sales_spend DESC
LIMIT 20;


-- =====================================================================
-- PHASE 6: ORDER METRICS, CANCELLATIONS & TIME PATTERNS
-- =====================================================================

-- Query 15: Average Order Value (AOV) & Basket Size (Using CTE)
-- What it does: Calculates total revenue per qualifying invoice inside a CTE, then finds the average order value.
-- Why we use it: Prevents double-counting by grouping at the invoice level first using a clean CTE.
WITH invoice_summary AS (
    SELECT 
        InvoiceNo,
        SUM(positive_sales_value) AS invoice_revenue,
        SUM(Quantity) AS invoice_quantity
    FROM
        online_retail_mysql
    WHERE
        is_cancellation = 0
            AND positive_sales_value > 0
    GROUP BY InvoiceNo
)
SELECT 
    COUNT(*) AS qualifying_invoices,
    ROUND(AVG(invoice_revenue), 2) AS average_qualifying_invoice_sales,
    ROUND(AVG(invoice_quantity), 2) AS average_qualifying_units_per_invoice
FROM
    invoice_summary;


-- Query 16A: Negative Quantity / Return-Like Transaction Lines
-- What it does: Summarizes all rows where Quantity is less than 0.
-- Why we use it: Separates physical unit returns and inventory adjustments from financial cancellations.
SELECT 
    COUNT(*) AS negative_quantity_rows,
    COUNT(DISTINCT InvoiceNo) AS invoices_with_negative_quantity,
    SUM(Quantity) AS signed_negative_quantity,
    SUM(ABS(Quantity)) AS absolute_negative_quantity
FROM
    online_retail_mysql
WHERE
    Quantity < 0;


-- Query 16B: Invoices Flagged as Cancellation Invoices
-- What it does: Summarizes distinct invoices, row counts, and line value for 'C' prefix cancellation invoices.
-- Why we use it: Tracks official cancellation invoices separately for Page 4 (Transaction Quality) of our dashboard.
SELECT 
    COUNT(DISTINCT InvoiceNo) AS cancellation_flagged_invoices,
    COUNT(*) AS rows_on_cancellation_flagged_invoices,
    ROUND(SUM(line_value), 2) AS line_value_on_flagged_invoices
FROM
    online_retail_mysql
WHERE
    is_cancellation_invoice = 1;


-- Query 16C: Negative-Value Transaction Lines
-- What it does: Counts negative-value rows and invoices, and sums their line values.
-- Why we use it: Measures negative transaction values separately from cancellation flags and negative quantities.
SELECT 
    COUNT(*) AS negative_value_rows,
    COUNT(DISTINCT InvoiceNo) AS invoices_with_negative_value,
    ROUND(SUM(line_value), 2) AS total_negative_line_value
FROM
    online_retail_mysql
WHERE
    line_value < 0;


-- Query 17: Sales by Day of Week & Hour of Day
-- What it does: Tracks shopping activity across weekdays and hours on positive sales rows.
-- Why we use it: Helps operations and marketing teams know the best days and peak hours to run promotions.
SELECT 
    day_of_week,
    COUNT(DISTINCT InvoiceNo) AS total_invoices,
    SUM(Quantity) AS total_quantity_on_positive_sales_rows,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value
FROM
    online_retail_mysql
WHERE
    is_cancellation = 0
        AND positive_sales_value > 0
GROUP BY day_of_week
ORDER BY positive_sales_value DESC;

SELECT 
    hour,
    COUNT(DISTINCT InvoiceNo) AS total_invoices,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value
FROM
    online_retail_mysql
WHERE
    is_cancellation = 0
        AND positive_sales_value > 0
GROUP BY hour
ORDER BY hour;


-- Query 18: Top 15 Actual Physical Products (Excluding Postage & Manual Fees)
-- What it does: Filters out non-merchandise codes (DOT, POST, M, etc.) before ranking top products.
-- Why we use it: Gives true merchandise rankings without shipping fees or manual accounting entries.
SELECT 
    StockCode,
    Description,
    COUNT(DISTINCT InvoiceNo) AS invoice_count,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(positive_sales_value), 2) AS positive_sales_value,
    RANK() OVER (ORDER BY SUM(positive_sales_value) DESC) AS product_rank
FROM
    online_retail_mysql
WHERE
    positive_sales_value > 0
    AND Description IS NOT NULL
    AND is_cancellation = 0
    AND StockCode NOT IN (
        'DOT', 'POST', 'M', 'AMAZONFEE',
        'B', 'CRUK', 'D', 'S', 'BANK CHARGES'
    )
GROUP BY StockCode , Description
ORDER BY positive_sales_value DESC
LIMIT 15;


-- =====================================================================
-- PHASE 7: QUERY OPTIMIZATION & PERFORMANCE AUDIT
-- =====================================================================

SELECT 
    ROUND(100.0 * COUNT(DISTINCT CASE
                    WHEN is_cancellation_invoice = 1 THEN InvoiceNo
                END) / NULLIF(COUNT(DISTINCT InvoiceNo), 0),
            2) AS cancellation_flagged_invoice_percentage
FROM
    online_retail_mysql;


-- Query 20: Inspect Existing Indexes & Evaluate Execution Plan
-- What it does: Displays all active indexes on the table and checks query execution plan using EXPLAIN.
-- Why we use it: To verify database optimization and demonstrate indexing awareness in interviews.
SHOW INDEX FROM online_retail_mysql;

EXPLAIN 
SELECT Country, ROUND(SUM(positive_sales_value), 2) AS country_sales
FROM online_retail_mysql
WHERE Country = 'Germany'
GROUP BY Country;

-- Pre-configured Index creation statements:
-- CREATE INDEX idx_invoice_no ON online_retail_mysql(InvoiceNo);
-- CREATE INDEX idx_customer_id ON online_retail_mysql(CustomerID);
-- CREATE INDEX idx_stock_code ON online_retail_mysql(StockCode);
-- CREATE INDEX idx_country ON online_retail_mysql(Country);
