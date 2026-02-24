Walmart Sales Data Analysis and Forecasting System

A hybrid analytics project combining Python-based forecasting and Power BI dashboard visualization to analyze Walmart sales performance and predict future revenue.

The project provides insights into:

Sales trends

Branch performance

Product categories

Customer behavior

Payment patterns

Revenue forecasting

Project Architecture

This project follows an end-to-end data analytics pipeline:

Walmart Sales Dataset (CSV)
        ↓
Data Cleaning & Feature Engineering (Python)
        ↓
Exploratory Data Analysis (Python)
        ↓
Time Series Forecasting (ARIMA Model)
        ↓
Forecast Dataset Export (CSV)
        ↓
Power BI Dashboard Visualization

This architecture integrates descriptive analytics + predictive analytics.

Project Components
1️⃣ Python Module

Python is used for:

Data preprocessing

Feature engineering

Time-series preparation

Forecast modeling

Model evaluation

Libraries Used
pandas
numpy
matplotlib
seaborn
statsmodels
scikit-learn
Data Processing Steps
Feature Engineering

New features created:

Month

Day

Year

Hour

Example:

Date → Month
Time → Hour
Time Series Preparation

Sales data was aggregated into daily revenue:

Date | Total Sales

This created a time series dataset suitable for forecasting.

File Generated:

DailySales.csv
Forecasting Model

The forecasting model uses:

ARIMA Model
ARIMA(5,1,2)

Used for predicting future sales trends.

Train-Test Split
80% Training
20% Testing
Model Evaluation

Forecast accuracy measured using:

MAE

Mean Absolute Error measures average prediction error.

RMSE

Root Mean Square Error penalizes large errors.

Lower values indicate better prediction performance.

Forecast Output

Future sales were predicted for:

Next 30 Days

Generated file:

FinalSalesForecast.csv

This file is integrated into Power BI.

Power BI Dashboard

Source PBIX:

WalmartSales.pbix

Dashboard analyzes:

Revenue trends

Branch performance

Product categories

Customer behavior

Payment analysis

Forecast visualization

Key Metrics

Total Revenue: ₹155.08K

Gross Income: ₹7.38K

Gross Margin: ~5%

Units Sold: 3K

Customers: 499

Avg Rating: 6.98

Forecast Visualization

The dashboard includes:

Actual vs Forecast Sales

Historical sales from Python

Predicted sales from ARIMA model

This provides decision support for future planning.

Dashboard Features
KPI Section

Total Revenue

Gross Income

Customer Count

Units Sold

Average Rating

Analysis Section

Monthly Sales Trend

Product Line Analysis

Branch Performance

Customer Analysis

Payment Analysis

Hourly Sales Pattern

Forecast Section

Forecast visualization includes:

Historical sales

Future predictions

Trend analysis

Important Measures (DAX)
Total Revenue
TotalRevenue = SUM(Sales[Total])
Gross Income
GrossIncome = SUM(Sales[Gross income])
Gross Margin %
GrossMarginPct =
DIVIDE([GrossIncome],[TotalRevenue])
Data Model

Recommended schema:

FactSales
   ↓
Date
Branch
Product Line
Customer
Payment

Star schema improves performance.

How to Run Python Part

Install libraries:

pip install pandas numpy matplotlib seaborn statsmodels scikit-learn

Run notebook:

sales_forecasting.ipynb

Output files:

DailySales.csv
FinalSalesForecast.csv
How to Open Power BI Dashboard

1 Install Power BI Desktop

2 Download PBIX file

3 Open WalmartSales.pbix

4 Refresh data if needed

Key Insights
Branch Performance

Branch C generates the highest revenue.

Product Performance

Food & Beverages and Electronics are strong contributors.

Customer Behavior

Customer distribution is balanced between genders and customer types.

Payment Trends

Digital payments show strong adoption.

Sales Patterns

Peak sales hours occur during afternoon and evening.

Suggested Improvements

Add Prophet or LSTM forecasting

Deploy Streamlit web app

Add real-time data

Improve model accuracy

Add profit forecasting

Tools Used

Python
Power BI
DAX
Power Query
Google Colab

Author

Barkha Jha
B.Tech CSE (Data Science)
Noida Institute of Engineering and Technology
