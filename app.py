import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np # Needed for mathematical operations

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Real Estate Investment Advisor", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    """Loads the final processed dataset."""
    df = pd.read_csv('processed_housing_data_final2.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'processed_housing_data_final2.csv' not found. Please ensure the file is in the same directory.")
    st.stop()

# --- SIDEBAR & NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Investment Advisor", "Market Analytics"])

# --- PAGE 1: HOME ---
if page == "Home":
    st.title("🏡 Real Estate Investment Advisor")
    st.markdown("""
    ### Project Goal: Predicting Property Profitability & Future Value
    
    This dashboard, developed as a Data Analytics tool, provides data-backed recommendations by:
    * **Forecasting** property prices over 5 years using a fixed growth rate.
    * **Classifying** properties as 'Good Investment' based on local market median prices.
    
    **👈 Select a page from the sidebar to get started.**
    """)
    
    st.subheader("Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Listings Analyzed", f"{len(df):,}")
    col2.metric("Avg Price (Lakhs)", f"₹ {df['Price_in_Lakhs'].mean():.2f} L")
    col3.metric("Cities Covered", len(df['City'].unique()))

# --- PAGE 2: INVESTMENT ADVISOR (Rule-Based Prediction) ---
elif page == "Investment Advisor":
    st.title("💰 Rule-Based Investment Estimator")
    st.markdown("Enter property details to receive an **Investment Recommendation** and **Future Value Forecast**.")

    # Input Form
    with st.form("investment_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_city = st.selectbox("Select City", df['City'].unique(), help="Used to filter localities.")
            # Filter localities based on city
            filtered_localities = df[df['City'] == selected_city]['Locality'].unique()
            selected_locality = st.selectbox("Select Locality", filtered_localities)
            
        with col2:
            current_price = st.number_input("Current Asking Price (in Lakhs)", min_value=1.0, value=50.0, step=1.0)
            bhk = st.number_input("BHK", min_value=1, max_value=10, value=2)
            
        submit_button = st.form_submit_button(label="Analyze Investment")

    # Logic Implementation (Simulating Classification & Regression)
    if submit_button:
        # 1. Classification Logic: Get Median Price for the selected Locality
        locality_median = df[df['Locality'] == selected_locality]['Price_in_Lakhs'].median()
        is_good_investment = current_price <= locality_median
        
        # 2. Regression Logic: Future Price (Compounding 8% for 5 years)
        growth_rate = 0.08
        years = 5
        future_price = current_price * ((1 + growth_rate) ** years)
        
        # --- DISPLAY RESULTS ---
        st.divider()
        st.subheader("📊 Recommendation")
        
        c1, c2 = st.columns(2)
        
        # Result 1: Classification
        with c1:
            if is_good_investment:
                st.success(f"✅ **Good Investment!** (Rule-Based)")
                st.write(f"Rationale: Price is **lower** than the locality median of ₹{locality_median:.2f} L.")
            else:
                st.warning(f"⚠️ **High Price Warning** (Rule-Based)")
                st.write(f"Rationale: Price is **higher** than the locality median of ₹{locality_median:.2f} L.")

        # Result 2: Regression (Future Price)
        with c2:
            st.info(f"📈 **Estimated Value in 5 Years**")
            st.metric(label="Future Price", value=f"₹ {future_price:.2f} Lakhs", delta=f"+{(future_price-current_price):.2f} L Estimated Appreciation")

# --- PAGE 3: MARKET ANALYTICS (EDA Dashboard) ---
elif page == "Market Analytics":
    st.title("📊 Market Insights Dashboard")
    st.markdown("Explore key trends and data distributions across the dataset.")
    
    # Filters
    st.sidebar.header("Filter Data")
    city_filter = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique()[:5])
    
    df_filtered = df[df['City'].isin(city_filter)]
    
    # ------------------
    # VISUAL INSIGHTS (Charts from EDA)
    # ------------------
    
    # Chart 1: Price Distribution (Question 1)
    st.subheader(f"Price Distribution in Selected Cities")
    fig_hist = px.histogram(df_filtered, x="Price_in_Lakhs", color="City", nbins=50, title="Price Range Distribution by City")
    st.plotly_chart(fig_hist, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # Chart 2: Avg Price per Sq Ft by Property Type (Question 3)
    with col1:
        st.subheader("Price per Sq Ft by Property Type")
        fig_box = px.box(df_filtered, x='Property_Type', y='Price_per_SqFt', color='Property_Type',
                         title="Price per Sq Ft across Property Types")
        st.plotly_chart(fig_box, use_container_width=True)

    # Chart 3: Investment Quality (Based on our target variable)
    with col2:
        st.subheader("Investment Quality Split")
        # Ensure 'Good_Investment' is mapped for readability
        df_filtered['Investment_Label'] = df_filtered['Good_Investment'].map({1: 'Good Investment', 0: 'High Price / Average'})
        fig_pie = px.pie(df_filtered, names='Investment_Label', title="Proportion of Investment Types")
        st.plotly_chart(fig_pie, use_container_width=True)
        