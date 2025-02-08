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

    # st.title("📊 Business Performance Dashboard")
    # st.markdown("### Interactive Job Metrics")
    # st.markdown('---')

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

    # Define CSS for rectangular KPI boxes
    st.markdown("""
        <style>
        .kpi-box {
            padding: 40px;
            border-radius: 20px;
            background-color: white;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            border: 2px solid #f0f2f6;
            width: 100%;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
            color: #007BFF;
        }
        .icon {
            font-size: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # col1.metric("Total Cost", format_number(total_cost))
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='icon'>💰</div>
            Total Cost<br>
            <span class='kpi-value'>{format_number(total_cost)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class = 'kpi-box'>
            <div class = 'icon'>📈</div>
            Total Revenue<br>
            <span class = 'kpi-value'>{format_number(total_revenue)}</span>
        </div>
        """,unsafe_allow_html = True)
        # col2.metric("Total Revenue", format_number(total_revenue))
    with col3:
        st.markdown(f"""
        <div class = 'kpi-box'>
            <div class = 'icon'>📊</div>
            Avg Margin<br>
            <span class = 'kpi-value'>{format_number(avg_margin)} %</span>
        </div>
        """,unsafe_allow_html = True)
        # col3.metric("Avg. Margin (%)", format_number(avg_margin ))

    with col4:
        st.markdown(f"""
        <div class = 'kpi-box'>
            <div class = 'icon'>📊</div>
            Jobs<br>
            <span class = 'kpi-value'>{filtered_df.shape[0]}</span>
        </div>
        """,unsafe_allow_html = True)
    st.markdown('---')

    col1, col2 = st.columns(2)

    with col1:
        ## Visualization: Margins by Job Type
        ## Bar Chart
        # st.subheader("Margins by Sector Name")
        # fig2 = px.bar(filtered_df, x='Sector Name', y=['Actual Cost', 'Actual Revenue'], barmode='group',
        #             title="Costs and Revenues by Job Type", labels={"value": "Amount", "variable": "Metric"})
        # st.plotly_chart(fig2)
        sector_summary = filtered_df.groupby("Sector Name")[["Actual Cost", "Actual Revenue"]].sum().reset_index()
        st.subheader("Revenue Distribution by Sector")
        fig2 = px.pie(sector_summary, 
              names="Sector Name", 
              values="Actual Revenue",  # You can change this to "Actual Cost" or another metric
              title="Revenue Distribution by Sector", 
              hole=0.4,  # Creates the donut effect
              color_discrete_sequence=px.colors.qualitative.Set3  # Color scheme
             )
        st.plotly_chart(fig2)
    with col2:
        # Visualization: Costs and Revenue by Job Type
        st.subheader("Cost and Revenue by Job Type")
        fig = px.bar(filtered_df, x='Job Type', y=['Actual Cost', 'Actual Revenue'], barmode='group',
                    title="Costs and Revenues by Job Type", labels={"value": "Amount", "variable": "Metric"})
        st.plotly_chart(fig)
    # Get top 5 Customers and Revenue contributions
    # st.subheader("Top Customers")
    top_customers = filtered_df.groupby('Customer Name').agg({'Actual Revenue':'sum'}).sort_values(ascending = False,by = 'Actual Revenue').reset_index().head()
    total_revenue = top_customers['Actual Revenue'].sum()
    top_customers["percentage"] = (top_customers['Actual Revenue']/total_revenue)*100
    st.subheader("Top 5 Customers by Revenue Contribution 🏆")
    for idx,row in top_customers.iterrows():
        col1,col2 = st.columns([3,4])
        with col1:
            st.markdown(f"{row['Customer Name']}")
        with col2:
            st.progress(float(row['percentage']/100))
            # st.caption(f"{format_number(row['Actual Revenue'])},{row['percentage']:.1f}%")
            st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between;">
                <span><b>💰 ₹{format_number(row['Actual Revenue'])}</b></span>
                <span><b>{row['percentage']:.1f}%</b></span>
            </div>
            """, 
            unsafe_allow_html=True
            )

    # Data Preview in an Expander
    rows = st.selectbox('Rows',options = [5,15,50,100],index = 0)
    with st.expander("📋 Data Preview ", expanded=True):
        st.dataframe(filtered_df.head(int(rows)))

else:
    st.info("Upload a file in the side bar.\nClick > if not visible")
