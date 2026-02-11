import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import os

# Set page config (First streamlit command)
st.set_page_config(page_title="Railway Seat Occupancy Dashboard", layout="wide")

# Constants
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/railway_booking_data.csv")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Data file not found at {DATA_PATH}. Please run generate_data.py first.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Options")
st.sidebar.markdown("**👨‍💻 Created by: Shubham Kumar**")
st.sidebar.markdown("---")

# Date Filter
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Convert to datetime for filtering
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Train Filter
train_ids = df['Train_ID'].unique()
selected_trains = st.sidebar.multiselect("Select Train IDs", train_ids, default=train_ids)

# Class Filter
classes = df['Class'].unique()
selected_classes = st.sidebar.multiselect("Select Classes", classes, default=classes)

# Filter Data
filtered_df = df[
    (df['Date'] >= start_date) & 
    (df['Date'] <= end_date) & 
    (df['Train_ID'].isin(selected_trains)) &
    (df['Class'].isin(selected_classes))
]

# Dashboard Title
st.title("🚄 Railway Seat Occupancy Analysis Dashboard")

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    # Key Metrics
    total_bookings = len(filtered_df)
    occupancy_rate = (filtered_df['Status'] == 'Booked').mean() * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{total_bookings:,}")
    col2.metric("Average Occupancy Rate", f"{occupancy_rate:.2f}%")
    col3.metric("Selected Trains", len(selected_trains))

    st.markdown("---")

    # Layout: 2 Columns for Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🔥 Seat Occupancy Heatmap (By Coach)")
        # Calculate occupancy by Coach and Date
        heatmap_data = filtered_df.groupby(['Coach', 'Date'])['Status'].apply(lambda x: (x == 'Booked').mean()).reset_index(name='Occupancy_Rate')
        
        if not heatmap_data.empty:
            pivot_table = heatmap_data.pivot_table(index='Coach', columns='Date', values='Occupancy_Rate', aggfunc='mean')
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(pivot_table, cmap="YlOrRd", ax=ax, cbar_kws={'label': 'Occupancy Rate'})
            ax.set_title("Daily Occupancy by Coach")
            st.pyplot(fig)
        else:
            st.info("Not enough data for heatmap.")

    with c2:
        st.subheader("📊 Occupancy by Class")
        class_occupancy = filtered_df.groupby('Class')['Status'].apply(lambda x: (x == 'Booked').mean()).reset_index(name='Occupancy_Rate')
        
        if not class_occupancy.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='Class', y='Occupancy_Rate', data=class_occupancy, palette="Blues_d", ax=ax)
            ax.set_ylim(0, 1)
            ax.set_ylabel("Occupancy Rate")
            st.pyplot(fig)
        else:
             st.info("Not enough data for bar chart.")

    # Second Row of Charts
    st.markdown("---")
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("🥧 Passenger Quota Distribution")
        quota_counts = filtered_df['Quota'].value_counts()
        if not quota_counts.empty:
            fig, ax = plt.subplots()
            ax.pie(quota_counts, labels=quota_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)
        else:
            st.info("No data for quota distribution.")

    with c4:
        st.subheader("📅 Occupancy by Day of Week")
        filtered_df['Day_Name'] = filtered_df['Date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_occupancy = filtered_df.groupby('Day_Name')['Status'].apply(lambda x: (x == 'Booked').mean()).reindex(day_order).reset_index(name='Occupancy_Rate')
        
        if not day_occupancy.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='Day_Name', y='Occupancy_Rate', data=day_occupancy, palette="viridis", ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax.set_ylim(0, 1)
            st.pyplot(fig)
        else:
            st.info("Not enough data for day of week analysis.")

    # Time Series Trend
    st.subheader("📈 Occupancy Trend Over Time")
    daily_trend = filtered_df.groupby('Date')['Status'].apply(lambda x: (x == 'Booked').mean()).reset_index(name='Occupancy_Rate')
    
    if not daily_trend.empty:
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.lineplot(x='Date', y='Occupancy_Rate', data=daily_trend, marker='o', ax=ax)
        ax.set_title("Average Daily Occupancy Trend")
        ax.set_ylim(0, 1)
        st.pyplot(fig)
    else:
        st.info("Not enough data for trend line.")

    # Data Preview
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df.head(100))
