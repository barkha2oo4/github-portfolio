import streamlit as st

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Walmart Sales Analytics System",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# HEADER SECTION
# -----------------------------

st.title("Walmart Sales Data Analysis and Forecasting System")

st.markdown("""
### End-to-End Data Science Project

This project presents a complete **Sales Analytics and Forecasting System**
developed using **Python, Machine Learning, and Power BI**.

The system analyzes Walmart retail sales data and provides insights into:

• Sales Performance  
• Customer Behavior  
• Product Demand  
• Revenue Trends  
• Future Sales Forecasting

The objective of this project is to build a **data-driven decision support system**
for retail business analysis.
""")

st.divider()


# -----------------------------
# EXECUTIVE SUMMARY
# -----------------------------

st.header("Executive Summary")

st.markdown("""
Retail businesses generate large volumes of transactional data.
However, extracting meaningful insights from this data can be challenging.

This project develops a complete analytics solution that helps businesses:

• Monitor sales performance  
• Understand customer behavior  
• Identify best-performing products  
• Analyze branch performance  
• Predict future revenue

The system integrates **Python Data Analysis**, **Machine Learning Models**,
and **Power BI Dashboards** into a single analytics platform.
""")

st.divider()


# -----------------------------
# KEY PERFORMANCE METRICS
# -----------------------------

st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Revenue",
    value="₹155K"
)

col2.metric(
    label="Total Customers",
    value="499"
)

col3.metric(
    label="Units Sold",
    value="3K"
)

col4.metric(
    label="Forecast Revenue",
    value="₹277K"
)

st.divider()
# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("Navigation Menu")

st.sidebar.markdown("""
Select a section to explore the project.
""")

page = st.sidebar.radio(
    "Go to Section:",
    [
        "Project Overview",
        "Business Understanding",
        "Dataset Description",
        "Sales Analysis",
        "Forecasting Models",
        "Power BI Dashboard",
        "Conclusion"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Project Information")

st.sidebar.markdown("""
Project Title:

Sales Data Analysis and Forecasting Dashboard

Tools Used:

• Python  
• Power BI  
• Machine Learning  
• Streamlit

Author:

Barkha Jha  
B.Tech CSE (Data Science)
""")

st.sidebar.markdown("---")
# -----------------------------
# PROJECT OVERVIEW PAGE
# -----------------------------

if page == "Project Overview":

    st.header("Project Overview")

    st.markdown("""
This project develops a **complete Sales Analytics and Forecasting System**
for analyzing Walmart retail data.

The system combines **data analysis**, **machine learning**, and **business intelligence**
to provide a comprehensive understanding of sales performance.

The project is designed to support **data-driven decision making**
in retail businesses.
""")

    st.subheader("Project Objectives")

    st.markdown("""
The main objectives of this project are:

• Analyze historical sales data

• Identify sales trends and patterns

• Understand customer purchasing behavior

• Evaluate product and branch performance

• Develop forecasting models

• Build interactive dashboard

• Provide business insights
""")

    st.subheader("Project Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
**Data Analysis Features**

• Monthly Sales Analysis

• Product Performance Analysis

• Branch Performance Analysis

• Customer Analysis

• Payment Analysis
""")

    with col2:

        st.markdown("""
**Forecasting Features**

• Time Series Forecasting

• ARIMA Model

• Linear Regression Model

• Model Comparison

• Forecast Visualization
""")

    st.subheader("System Architecture")

    st.info("""
Walmart Dataset → Python Processing → Forecast Models → Power BI Dashboard → Web Application
""")

    st.subheader("Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
**Python**

• Pandas

• Numpy

• Matplotlib

• Statsmodels
""")

    with col2:

        st.markdown("""
**Machine Learning**

• ARIMA Model

• Linear Regression

• Forecast Evaluation
""")

    with col3:

        st.markdown("""
**Visualization**

• Power BI Dashboard

• Interactive Filters

• KPI Monitoring
""")
# -----------------------------
# BUSINESS UNDERSTANDING PAGE
# -----------------------------

elif page == "Business Understanding":

    st.header("Business Understanding")

    st.markdown("""
Understanding the business context is essential for building
an effective analytics system.

Retail companies generate large volumes of sales transactions
every day. Analyzing this data helps organizations improve
decision-making and operational efficiency.
""")

    st.subheader("About Walmart")

    st.markdown("""
Walmart is one of the largest retail companies in the world,
operating supermarkets and retail stores across multiple cities.

Retail businesses like Walmart sell thousands of products
to customers daily and generate large volumes of transactional data.

Analyzing this data helps businesses:

• Monitor sales performance

• Improve customer satisfaction

• Optimize inventory

• Increase profitability

• Predict future demand
""")

    st.subheader("Business Problems")

    st.markdown("""
Retail managers often face challenges such as:

• Difficulty tracking branch performance

• Identifying best-selling products

• Understanding customer behavior

• Monitoring revenue trends

• Predicting future sales

Traditional reporting systems are often slow and do not provide
real-time insights.
""")

    st.subheader("Business Questions Answered")

    st.markdown("""
This project helps answer important business questions:

• Which branch generates the highest revenue?

• Which product categories perform best?

• When do customers shop the most?

• Which payment methods are preferred?

• How will sales change in the future?
""")

    st.subheader("Project Objectives")

    st.markdown("""
The goal of this project is to develop a data-driven system that:

• Analyzes Walmart sales data

• Identifies business trends

• Provides actionable insights

• Predicts future revenue

• Supports strategic decision-making
""")
# -----------------------------
# DATASET DESCRIPTION PAGE
# -----------------------------

elif page == "Dataset Description":

    st.header("Dataset Description")

    st.markdown("""
This project uses a **Walmart Sales Dataset** containing retail
transaction data.

The dataset contains sales transactions including product details,
customer information, payment methods, and sales values.

The dataset was used to analyze sales patterns and develop
forecasting models.
""")

    st.subheader("Dataset Size")

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Total Records", "1000")

        st.metric("Total Features", "17")

    with col2:

        st.metric("Time Period", "3 Months")

        st.metric("Cities", "3")



    st.subheader("Dataset Features")

    st.markdown("""
The dataset contains the following important features:

• Invoice ID – Unique transaction identifier

• Branch – Store branch (A, B, C)

• City – Store location

• Customer Type – Member or Normal

• Gender – Male or Female

• Product Line – Product category

• Unit Price – Price per item

• Quantity – Number of items sold

• Total – Total transaction value

• Date – Transaction date

• Time – Transaction time

• Payment – Payment method

• Rating – Customer rating
""")


    st.subheader("Data Preprocessing")

    st.markdown("""
The dataset was processed using Python before analysis.

The following preprocessing steps were performed:

• Missing values were checked

• Date column converted into datetime format

• Time column converted into hour format

• New features created (Month, Day, Hour)

• Duplicate records checked

• Data validated for consistency
""")


    st.subheader("Feature Engineering")

    st.markdown("""
Additional features were created to improve analysis.

New features include:

• Month – Extracted from Date

• Day – Extracted from Date

• Hour – Extracted from Time

These features helped analyze time-based sales patterns.
""")


    st.subheader("Time Series Dataset")

    st.markdown("""
For forecasting purposes, the dataset was converted into
a time series format.

Daily sales were calculated by aggregating transaction data.

The time series dataset contains:

Date → Daily Total Sales

This dataset was used to train forecasting models.
""")


    st.success("""
DailySales.csv was generated and used for forecasting models.
""")
# -----------------------------
# SALES ANALYSIS PAGE
# -----------------------------

elif page == "Sales Analysis":

    st.header("Sales Data Analysis")

    st.markdown("""
This section presents the results obtained from analyzing
the Walmart sales dataset.

The analysis helps understand sales performance,
customer behavior, and business trends.
""")

    st.subheader("Overall Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue","₹155K")
    col2.metric("Total Customers","499")
    col3.metric("Units Sold","3K")
    col4.metric("Average Rating","6.9")



    st.subheader("Key Findings")

    st.markdown("""
The following insights were obtained from the sales analysis:

• Total revenue reached approximately ₹155K indicating stable business performance.

• Branch C generated the highest revenue among all branches.

• Product categories contributed evenly to total sales.

• Customer distribution is balanced across genders.

• Both member and normal customers contribute significantly.

• Digital payment methods are widely used by customers.
""")


    st.subheader("Branch Performance Analysis")

    st.markdown("""
Branch-level analysis shows differences in sales performance.

• Branch C shows the highest revenue.

• Branch A and Branch B show similar performance levels.

• High-performing branches may have better product availability
  and customer traffic.
""")


    st.subheader("Product Line Analysis")

    st.markdown("""
Product line analysis helps identify important categories.

• Food & Beverages generate significant revenue.

• Electronic Accessories show strong performance.

• Sports & Travel products contribute steadily.

Balanced product performance indicates diversified demand.
""")


    st.subheader("Customer Behavior Analysis")

    st.markdown("""
Customer analysis provides insights into purchasing behavior.

• Male and Female customers contribute nearly equally.

• Member customers tend to purchase more frequently.

• Customer ratings indicate moderate satisfaction levels.
""")


    st.subheader("Time-Based Sales Patterns")

    st.markdown("""
Time-based analysis helps understand shopping patterns.

• Peak sales occur during afternoon and evening hours.

• Sales activity increases after midday.

• Evening hours show high customer traffic.

Understanding peak hours helps optimize staffing and inventory.
""")


    st.subheader("Payment Method Analysis")

    st.markdown("""
Payment method analysis shows customer preferences.

• Cash payments remain common.

• Credit card usage is significant.

• E-wallet payments are increasing.

Digital payment growth indicates changing customer behavior.
""")


    st.subheader("Business Insights")

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("""
**Operational Insights**

• High sales during afternoon hours

• Some branches outperform others

• Product demand varies

• Customer ratings can improve
""")

    with col2:

        st.markdown("""
**Strategic Insights**

• Improve marketing in low-sales periods

• Increase stock for high-demand products

• Improve customer experience

• Promote digital payments
""")



    st.subheader("Statistical Summary")

    st.markdown("""
Basic statistical analysis helps understand sales distribution.

• Average transaction value shows typical purchase size.

• Standard deviation shows variation in sales.

• Minimum and maximum values indicate sales range.

Statistical analysis helps understand data behavior.
""")
# -----------------------------
# FORECASTING MODELS PAGE
# -----------------------------

elif page == "Forecasting Models":

    st.header("Sales Forecasting Models")

    st.markdown("""
Forecasting future sales is an important part of retail analytics.

This project uses **Machine Learning and Time Series Models**
to predict future Walmart sales.

Forecasting helps businesses:

• Plan inventory

• Estimate revenue

• Optimize staffing

• Improve decision making
""")

    st.subheader("Time Series Forecasting")

    st.markdown("""
Sales data is time-dependent because sales occur over time.

To perform forecasting, transaction data was converted into
a **daily time series dataset**.

Daily total sales were calculated for each date and used
to train forecasting models.
""")



    st.subheader("ARIMA Forecasting Model")

    st.markdown("""
ARIMA stands for:

AutoRegressive Integrated Moving Average

ARIMA models use past values and past errors to predict future values.

The ARIMA model used in this project:

ARIMA(5,1,2)

This model captures time-based patterns in sales data.
""")



    st.subheader("Linear Regression Model")

    st.markdown("""
Linear Regression is a machine learning algorithm
used to model relationships between variables.

In this project:

• Date was converted into numeric values

• Sales were predicted using regression

Linear Regression provides a baseline comparison model.
""")



    st.subheader("Model Comparison")

    st.markdown("""
Two models were compared:

• ARIMA Model

• Linear Regression Model

ARIMA performed better because it captures time dependencies
in sales data.
""")



    st.subheader("Forecast Accuracy")

    col1,col2 = st.columns(2)

    with col1:

        st.metric("MAE","Low")

        st.metric("RMSE","Low")

    with col2:

        st.write("""
MAE (Mean Absolute Error)

Measures average prediction error.
""")

        st.write("""
RMSE (Root Mean Square Error)

Penalizes large prediction errors.
""")



    st.subheader("Confidence Interval Forecast")

    st.markdown("""
Forecasting includes uncertainty.

Confidence intervals show the expected range
of future sales values.

This helps businesses understand prediction reliability.
""")



    st.subheader("Forecast Results")

    st.markdown("""
The forecasting model predicts **stable future sales trends**
based on historical data.

The model indicates that sales are expected to remain
consistent in upcoming periods.
""")
# -----------------------------
# POWER BI DASHBOARD PAGE
# -----------------------------

elif page == "Power BI Dashboard":

    st.header("Power BI Sales Dashboard")

    st.markdown("""
The Power BI dashboard provides an **interactive visualization**
of Walmart sales performance.

The dashboard allows users to explore:

• Revenue trends

• Branch performance

• Product performance

• Customer behavior

• Payment methods

• Forecast results
""")



    st.subheader("Dashboard Features")

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("""
**KPI Monitoring**

• Total Revenue

• Gross Income

• Customer Count

• Units Sold

• Average Rating
""")

    with col2:

        st.markdown("""
**Interactive Analysis**

• Sales by Branch

• Sales by Product

• Sales by Month

• Sales by Hour

• Payment Analysis
""")


    st.subheader("Dashboard Benefits")

    st.markdown("""
The dashboard helps businesses:

• Monitor performance

• Identify trends

• Compare branches

• Track customer behavior

• Support decision making
""")


    st.subheader("Forecast Integration")

    st.markdown("""
Forecast results generated in Python were integrated
into the Power BI dashboard.

This allows users to compare:

• Historical Sales

• Predicted Sales

The integration provides a complete analytics system.
""")



    st.subheader("Open Interactive Dashboard")

    st.write("""
Click below to open the live Power BI dashboard.
""")

    dashboard_link = "https://app.powerbi.com/links/i4htP_tevM?ctid=61363c43-8420-43ca-8f82-801627e16cdf&pbi_source=linkShare"

    st.link_button(
        "Open Power BI Dashboard",
        dashboard_link
    )
# -----------------------------
# CONCLUSION PAGE
# -----------------------------

elif page == "Conclusion":

    st.header("Project Conclusion")

    st.markdown("""
This project successfully developed a **Sales Data Analysis and Forecasting System**
for Walmart retail data.

The system integrates **data analysis, machine learning, and dashboard visualization**
to provide meaningful business insights.

The project demonstrates how data science techniques can be used
to support business decision-making.
""")


    st.subheader("Project Achievements")

    st.markdown("""
The following objectives were achieved:

• Sales data successfully analyzed

• Customer behavior understood

• Product performance evaluated

• Branch performance compared

• Forecasting models developed

• Dashboard created

• Web application developed
""")


    st.subheader("Key Results")

    st.markdown("""
Major outcomes of the project include:

• Identification of sales trends

• Understanding of customer behavior

• Performance comparison across branches

• Forecasting future sales

• Development of interactive dashboard
""")


    st.subheader("Project Limitations")

    st.markdown("""
Some limitations of this project include:

• Dataset contains only three months of data

• Long-term forecasting accuracy is limited

• Dataset size is relatively small

• Real-time data was not available

Despite these limitations, the project provides
useful business insights.
""")


    st.subheader("Future Scope")

    st.markdown("""
This project can be improved in the future by:

• Using larger datasets

• Implementing deep learning models such as LSTM

• Adding real-time data integration

• Deploying cloud-based analytics systems

• Improving forecasting accuracy

• Developing mobile dashboards
""")


    st.subheader("Learning Outcomes")

    st.markdown("""
Skills developed during this project:

• Data Cleaning and Preprocessing

• Exploratory Data Analysis

• Machine Learning Forecasting

• Power BI Dashboard Development

• Data Visualization

• Web Application Development
""")


    st.success("""
End-to-End Sales Analytics System using Python and Power BI.
""")