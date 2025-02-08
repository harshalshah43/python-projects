import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Interactive Job Metrics Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)


    # Display data preview
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Dropdowns for filtering
    sectors = ['All'] + df['Sector Name'].unique().tolist()
    locations = ['All'] + df['Location'].unique().tolist()

    selected_sector = st.selectbox("Select Sector:", options=sectors, index=0)
    selected_location = st.selectbox("Select Location:", options=locations, index=0)

    filtered_df = df.copy()

    # Filtered data
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df['Business Vertical'] == selected_sector]
    if selected_location != "All":
        filtered_df = filtered_df[filtered_df['Location'] == selected_location]

    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df)

    # KPIs
    st.subheader("Key Metrics")
    total_cost = filtered_df['Actual Cost'].sum()
    total_revenue = filtered_df['Actual Revenue'].sum()
    avg_margin = filtered_df['Actual Margin %'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"{total_cost:,.2f}")
    col2.metric("Total Revenue", f"{total_revenue:,.2f}")
    col3.metric("Avg. Margin (%)", f"{avg_margin:.2f}%")

    # Visualization: Costs and Revenue by Job Type
    st.subheader("Cost and Revenue by Job Type")
    fig = px.bar(filtered_df, x='Job Type', y=['Actual Cost', 'Actual Revenue'], barmode='group',
                 title="Costs and Revenues by Job Type", labels={"value": "Amount", "variable": "Metric"})
    st.plotly_chart(fig)

    # Visualization: Margins by Job Type
    st.subheader("Margins by Job Type")
    fig2 = px.box(filtered_df, x='Job Type', y='Actual Margin %',
                  title="Margins by Job Type", labels={"Actual Margin %": "Margin %"})
    st.plotly_chart(fig2)

else:
    st.info("Please upload a file to get started.")
