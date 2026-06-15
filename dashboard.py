import streamlit as st
import pandas as pd
import plotly.express as px
import os
from glob import glob

# Page Config
st.set_page_config(page_title="HealthCost Lens Dashboard", layout="wide")

st.title("HealthCost Lens: Medicare Analytics Dashboard")
st.markdown("### Distributed Analysis of Provider Cost, Access, and Anomalies")

# Helper function to handle your header-enabled Spark outputs
def load_data(folder_name):
    # Adjust path to where you exported the folders
    path = f"final_output/hive_results/{folder_name}/part-*.csv"
    files = glob(path)
    if files:
        # Since hive_queries.py used .option("header", True), read directly
        return pd.read_csv(files[0])
    return None

# --- SIDEBAR: Project Metrics ---
st.sidebar.header("Model Performance")
st.sidebar.metric("Random Forest RMSE", "208.65")
st.sidebar.metric("Random Forest R²", "0.2781")
st.sidebar.write("Primary Driver: Submitted Charge (~96%)")

# --- MAIN TABBED INTERFACE ---
tab1, tab2, tab3, tab4 = st.tabs(["Geographic Analysis", "Anomalies & Access", "Specialty Trends", "ML Insights"])

with tab1:
    st.header("Geographic Payout Distribution")
    df_q1 = load_data("q1_payment_by_state")
    if df_q1 is not None:
        procs = df_q1['proc_code'].unique()
        selected_proc = st.selectbox("Select Procedure Code", procs)
        map_df = df_q1[df_q1['proc_code'] == selected_proc]
        
        fig = px.choropleth(map_df, 
                            locations='state', 
                            locationmode="USA-states", 
                            color='avg_payment',
                            scope="usa",
                            color_continuous_scale="Reds",
                            title=f"Avg Payout for {selected_proc}")
        st.plotly_chart(fig, width='stretch')

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.header("High-Billing Outliers")
        df_q2 = load_data("q2_outliers") # Matches path in hive_queries.py
        if df_q2 is not None:
            st.write("Top providers by Z-Score (Charge variance from average)")
            st.dataframe(df_q2, height=400)
    
    with col_b:
        st.header("Geographic Access Gap")
        df_q3 = load_data("q3_access_gap")
        if df_q3 is not None:
            # Uses 'bene_per_provider' column from your SQL
            fig3 = px.bar(df_q3.head(15), x='state', y='bene_per_provider', color='specialty',
                          title="Highest Patients-per-Provider by State")
            st.plotly_chart(fig3, width='stretch')

with tab3:
    st.header("Cost & Volume Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Procedure Cost Disparity")
        df4 = load_data("q4_yoy_trend")
        if df4 is not None and not df4.empty:
            # Matches new columns: proc_code, avg_charge, avg_payment
            fig4 = px.bar(df4.head(15), x='proc_code', y=['avg_charge', 'avg_payment'], 
                          barmode='group', title="Charge vs. Actual Medicare Payout")
            st.plotly_chart(fig4, width='stretch')

    with col2:
        st.subheader("Top Specialty Volume")
        df_q5 = load_data("q5_specialty_volume") # Matches path in hive_queries.py
        if df_q5 is not None:
            fig5 = px.pie(df_q5.head(10), values='total_payment_volume', names='specialty', 
                          title="Top 10 Specialties by Total Payment Volume")
            st.plotly_chart(fig5, width='stretch')

with tab4:
    st.header("Machine Learning Deliverables")
    m1, m2 = st.columns(2)
    
    with m1:
        st.subheader("K-Means Optimization")
        if os.path.exists("elbow_plot.png"):
            st.image("elbow_plot.png", caption="Elbow plot identifying k=4 as optimal")

    with m2:
        st.subheader("Random Forest Feature Importance")
        if os.path.exists("feature_importance.png"):
            st.image("feature_importance.png", caption="Submitted Charge is the dominant predictor")
