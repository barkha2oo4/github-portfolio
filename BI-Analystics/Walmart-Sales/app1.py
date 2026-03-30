import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Walmart Sales Analytics | Enterprise Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/barkha-jha/',
        'Report a bug': None,
        'About': '### Walmart Sales Analytics System v2.0\nBuilt with ❤️ using Streamlit'
    }
)

# ============================================
# CUSTOM CSS FOR PROFESSIONAL UI
# ============================================

st.markdown("""
<style>
    /* Main Theme */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }

    /* KPI Cards */
    .kpi-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Text */
    p, div, label {
        color: rgba(255,255,255,0.9) !important;
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
    }

    /* DataFrames */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }

    /* Success/Info/Warning Messages */
    .stAlert {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0,0,0,0.3);
        padding: 15px;
        text-align: center;
        color: rgba(255,255,255,0.6);
        font-size: 12px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MOCK DATA GENERATION (Replace with real data)
# ============================================

@st.cache_data
def generate_sample_data():
    """Generate realistic sample data for the dashboard"""
    np.random.seed(42)
    n_records = 1000

    # Generate dates for 3 months
    dates = pd.date_range(start='2023-01-01', end='2023-03-31', freq='h')

    # Create dataframe
    data = {
        'Invoice ID': [f'INV-{str(i).zfill(6)}' for i in range(1, n_records + 1)],
        'Branch': np.random.choice(['A', 'B', 'C'], n_records, p=[0.35, 0.30, 0.35]),
        'City': np.random.choice(['Yangon', 'Mandalay', 'Naypyitaw'], n_records, p=[0.35, 0.30, 0.35]),
        'Customer Type': np.random.choice(['Member', 'Normal'], n_records, p=[0.5, 0.5]),
        'Gender': np.random.choice(['Male', 'Female'], n_records),
        'Product Line': np.random.choice([
            'Health and Beauty', 'Electronic Accessories',
            'Food and Beverages', 'Sports and Travel',
            'Fashion Accessories', 'Home and Lifestyle'
        ], n_records, p=[0.15, 0.20, 0.18, 0.17, 0.15, 0.15]),
        'Unit Price': np.round(np.random.uniform(10, 100, n_records), 2),
        'Quantity': np.random.randint(1, 10, n_records),
        'Tax 5%': np.zeros(n_records),
        'Total': np.zeros(n_records),
        'Date': np.random.choice(pd.date_range('2023-01-01', '2023-03-31'), n_records),
        'Time': np.random.choice(pd.date_range('2023-01-01', periods=12, freq='h').time, n_records),
        'Payment': np.random.choice(['Cash', 'Credit Card', 'Ewallet'], n_records, p=[0.3, 0.4, 0.3]),
        'cogs': np.zeros(n_records),
        'gross margin percentage': np.zeros(n_records),
        'gross income': np.zeros(n_records),
        'Rating': np.round(np.random.uniform(4, 10, n_records), 1)
    }

    df = pd.DataFrame(data)

    # Calculate derived fields
    df['Total'] = (df['Unit Price'] * df['Quantity'] * 1.05).round(2)
    df['cogs'] = (df['Total'] / 1.05).round(2)
    df['gross income'] = (df['Total'] - df['cogs']).round(2)
    df['gross margin percentage'] = ((df['gross income'] / df['Total']) * 100).round(2)

    # Add hour for time analysis
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day_name()
    df['DayOfMonth'] = df['Date'].dt.day

    return df

# ============================================
# SIDEBAR FILTERS
# ============================================

def render_sidebar_filters(df):
    """Render interactive filters in sidebar"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: white; margin: 0;">🛒 Walmart</h2>
        <p style="color: rgba(255,255,255,0.7); margin: 5px 0;">Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # Logo/Title
    st.sidebar.markdown("### 🎯 Filters & Settings")

    # Date Range Filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()

    date_range = st.sidebar.date_input(
        "📅 Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Branch Filter
    all_branches = ['All'] + sorted(df['Branch'].unique().tolist())
    selected_branch = st.sidebar.selectbox("🏬 Select Branch", all_branches)

    # City Filter
    all_cities = ['All'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox("🌆 Select City", all_cities)

    # Product Line Filter
    all_products = ['All'] + sorted(df['Product Line'].unique().tolist())
    selected_product = st.sidebar.selectbox("📦 Select Product Line", all_products)

    # Customer Type Filter
    all_customers = ['All'] + sorted(df['Customer Type'].unique().tolist())
    selected_customer = st.sidebar.selectbox("👥 Customer Type", all_customers)

    # Apply Filters
    filtered_df = df.copy()

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Date'] >= pd.to_datetime(date_range[0])) &
            (filtered_df['Date'] <= pd.to_datetime(date_range[1]))
        ]

    if selected_branch != 'All':
        filtered_df = filtered_df[filtered_df['Branch'] == selected_branch]

    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Product Line'] == selected_product]

    if selected_customer != 'All':
        filtered_df = filtered_df[filtered_df['Customer Type'] == selected_customer]

    st.sidebar.markdown("---")

    # Display filter stats
    st.sidebar.markdown("### 📊 Data Summary")
    st.sidebar.write(f"**Total Records:** {len(filtered_df):,}")
    st.sidebar.write(f"**Date Range:** {filtered_df['Date'].min().strftime('%b %d')} - {filtered_df['Date'].max().strftime('%b %d, %Y')}")

    return filtered_df, date_range

# ============================================
# KPI CARDS
# ============================================

def render_kpi_cards(filtered_df, original_df):
    """Render interactive KPI cards"""

    # Calculate metrics
    total_revenue = filtered_df['Total'].sum()
    total_customers = filtered_df['Invoice ID'].nunique()
    total_units = filtered_df['Quantity'].sum()
    avg_rating = filtered_df['Rating'].mean()
    avg_transaction = filtered_df['Total'].mean()
    gross_income = filtered_df['gross income'].sum()

    # Calculate deltas (comparison with original)
    rev_delta = ((total_revenue - original_df['Total'].sum()) / original_df['Total'].sum()) * 100
    cust_delta = ((total_customers - original_df['Invoice ID'].nunique()) / original_df['Invoice ID'].nunique()) * 100

    # Create columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div class="kpi-card" style="text-align: center;">
            <p style="font-size: 14px; opacity: 0.8; margin: 0;">💰 Total Revenue</p>
            <h2 style="font-size: 28px; margin: 10px 0; color: #00ff88;">${total_revenue:,.0f}</h2>
            <p style="font-size: 12px; opacity: 0.6;">vs total: {rev_delta:+.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card" style="text-align: center;">
            <p style="font-size: 14px; opacity: 0.8; margin: 0;">👥 Total Transactions</p>
            <h2 style="font-size: 28px; margin: 10px 0; color: #00d4ff;">{total_customers:,}</h2>
            <p style="font-size: 12px; opacity: 0.6;">vs total: {cust_delta:+.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="kpi-card" style="text-align: center;">
            <p style="font-size: 14px; opacity: 0.8; margin: 0;">📦 Units Sold</p>
            <h2 style="font-size: 28px; margin: 10px 0; color: #ff6b6b;">{total_units:,}</h2>
            <p style="font-size: 12px; opacity: 0.6;">Average: {total_units/len(filtered_df):.1f}/order</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="kpi-card" style="text-align: center;">
            <p style="font-size: 14px; opacity: 0.8; margin: 0;">⭐ Avg Rating</p>
            <h2 style="font-size: 28px; margin: 10px 0; color: #ffd93d;">{avg_rating:.1f}</h2>
            <p style="font-size: 12px; opacity: 0.6;">Gross Income: ${gross_income:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

    return {
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_units': total_units,
        'avg_rating': avg_rating,
        'avg_transaction': avg_transaction,
        'gross_income': gross_income
    }

# ============================================
# CHARTS
# ============================================

def render_charts(filtered_df):
    """Render interactive charts using Plotly"""

    # Tab structure for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Revenue Analysis",
        "🏬 Branch Performance",
        "📦 Product Insights",
        "👥 Customer Analysis",
        "⏰ Time Patterns"
    ])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Monthly Revenue Trend
            monthly_data = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Total'].sum().reset_index()
            monthly_data['Date'] = monthly_data['Date'].astype(str)

            fig = px.line(monthly_data, x='Date', y='Total', title='Monthly Revenue Trend')
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Daily Revenue
            daily_data = filtered_df.groupby('DayOfMonth')['Total'].sum().reset_index()

            fig = px.bar(daily_data, x='DayOfMonth', y='Total', title='Daily Revenue Distribution')
            st.plotly_chart(fig, width='stretch')

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            # Branch Revenue
            branch_data = filtered_df.groupby('Branch')['Total'].sum().reset_index()

            fig = px.pie(branch_data, values='Total', names='Branch', title='Revenue by Branch')
            st.plotly_chart(fig, width='stretch')

        with col2:
            # City Revenue
            city_data = filtered_df.groupby('City')['Total'].sum().reset_index()

            fig = px.bar(city_data, x='City', y='Total', title='Revenue by City')
            st.plotly_chart(fig, width='stretch')

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            # Product Line Revenue
            product_data = filtered_df.groupby('Product Line')['Total'].sum().reset_index()

            fig = px.bar(product_data, x='Product Line', y='Total', title='Revenue by Product Line')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Product Line Quantity
            product_qty = filtered_df.groupby('Product Line')['Quantity'].sum().reset_index()

            fig = px.pie(product_qty, values='Quantity', names='Product Line', title='Units Sold by Product Line')
            st.plotly_chart(fig, width='stretch')

    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            # Customer Type Revenue
            customer_data = filtered_df.groupby('Customer Type')['Total'].sum().reset_index()

            fig = px.bar(customer_data, x='Customer Type', y='Total', title='Revenue by Customer Type')
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Gender Distribution
            gender_data = filtered_df.groupby('Gender')['Total'].sum().reset_index()

            fig = px.pie(gender_data, values='Total', names='Gender', title='Revenue by Gender')
            st.plotly_chart(fig, width='stretch')

    with tab5:
        col1, col2 = st.columns(2)

        with col1:
            # Hourly Sales
            hourly_data = filtered_df.groupby('Hour')['Total'].sum().reset_index()

            fig = px.line(hourly_data, x='Hour', y='Total', title='Sales by Hour of Day')
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Day of Week
            day_data = filtered_df.groupby('Day')['Total'].sum().reset_index()

            fig = px.bar(day_data, x='Day', y='Total', title='Sales by Day of Week')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, width='stretch')

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application function"""

    # Load data
    with st.spinner("Loading data..."):
        df = generate_sample_data()

    # Render sidebar filters
    filtered_df, date_range = render_sidebar_filters(df)

    # Main content
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: white; margin: 0;">🏪 Walmart Sales Analytics Dashboard</h1>
        <p style="color: rgba(255,255,255,0.7); margin: 10px 0; font-size: 18px;">Enterprise-Level Retail Analytics & Insights</p>
    </div>
    """, unsafe_allow_html=True)

    # Render KPI cards
    kpis = render_kpi_cards(filtered_df, df)

    st.markdown("---")

    # Render charts
    render_charts(filtered_df)

    # Data table
    st.markdown("### 📋 Raw Data Preview")
    with st.expander("View Sample Data"):
        st.dataframe(filtered_df.head(50), width='stretch')

    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2024 Walmart Sales Analytics | Built with Streamlit | Data Science Project</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()