import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(page_title="Interactive Job Metrics", layout="wide")  # Wide layout
st.sidebar.title("File Upload")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)


    # Display data preview
    # st.subheader("Data Preview")
    # st.dataframe(df.head(3))

    with st.sidebar:
        st.sidebar.subheader('Filters')
        # Dropdowns for filtering
        # year = ['All'] + df['']
        sectors = ['All'] + df['Sector Name'].unique().tolist()
        locations = ['All'] + df['Location'].unique().tolist()

        selected_sector = st.selectbox("Select Sector:", options=sectors, index=0)
        selected_location = st.selectbox("Select Location:", options=locations, index=0)

    filtered_df = df.copy()

    # Filtered data
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df['Sector Name'] == selected_sector]
    if selected_location != "All":
        filtered_df = filtered_df[filtered_df['Location'] == selected_location]

    # st.subheader("Filtered Data Preview")
    # st.dataframe(filtered_df)

    st.title("📊 Business Performance Dashboard")
    st.markdown("### Interactive Job Metrics")
    st.markdown('---')

    def format_number(value):
        if value >= 1_000_000_000:  # Billions
            return f"{value / 1_000_000_000:.1f} B"
        elif value >= 1_000_000:  # Millions
            return f"{value / 1_000_000:.1f} M"
        else:
            return f"{value:,.2f}"  # Normal number formatting

    # KPIs
    st.subheader("Key Metrics")
    total_cost = filtered_df['Actual Cost'].sum()
    total_revenue = filtered_df['Actual Revenue'].sum()
    avg_margin = filtered_df['Actual Margin %'].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        col1.metric("Total Cost", format_number(total_cost))
    with col2:
        col2.metric("Total Revenue", format_number(total_revenue))
    with col3:
        col3.metric("Avg. Margin (%)", format_number(avg_margin ))
    st.markdown('---')

    col1, col2 = st.columns(2)

    with col1:
        # Visualization: Costs and Revenue by Job Type
        st.subheader("Cost and Revenue by Job Type")
        fig = px.bar(filtered_df, x='Job Type', y=['Actual Cost', 'Actual Revenue'], barmode='group',
                    title="Costs and Revenues by Job Type", labels={"value": "Amount", "variable": "Metric"})
        st.plotly_chart(fig)

    with col2:
        # Visualization: Margins by Job Type
        st.subheader("Margins by Job Type")
        fig2 = px.bar(filtered_df, x='Job Type', y=['Actual Cost', 'Actual Revenue'], barmode='group',
                    title="Costs and Revenues by Job Type", labels={"value": "Amount", "variable": "Metric"})
        st.plotly_chart(fig2)

    # Get top 5 Customers and Revenue contributions

    # Data Preview in an Expander
    rows = st.selectbox('Rows',options = [5,15,50,100],index = 0)
    with st.expander("📋 Data Preview ", expanded=True):
        st.dataframe(filtered_df.head(int(rows)))

else:
    st.info("Upload a file in the side bar.\nClick > if not visible")
