import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px

# Path to the folder where PySpark writes the JSON files
json_data_path = '/data/output/processed_trips/'

# Function to load JSON data into a DataFrame with error handling
def load_json_data(path):
    try:
        if not os.path.exists(path):
            st.error(f"Path does not exist: {path}")
            return pd.DataFrame()  # Return an empty DataFrame if the path doesn't exist
        
        json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]
        if len(json_files) == 0:
            st.warning("No JSON files found in the directory.")
            return pd.DataFrame()

        data = []
        for file_name in json_files:
            with open(os.path.join(path, file_name), 'r') as file:
                for line in file:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        st.error(f"Error decoding JSON in file {file_name}: {e}")
                        continue
        if len(data) == 0:
            st.warning("No data loaded from JSON files.")
            return pd.DataFrame()

        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

# Load and display the data
st.title("NYC Taxi Trips Data with Graphs")

try:
    df = load_json_data(json_data_path)
    
    if df.empty:
        st.warning("No data available to display.")
    else:
        st.dataframe(df)

        # Basic statistics
        st.subheader("Basic Statistics")
        st.write(df.describe())

        # Plot: Trip Duration Distribution
        st.subheader("Trip Duration Distribution")
        try:
            fig_duration = px.histogram(df, x='duration', nbins=50, title='Trip Duration Distribution', labels={'duration':'Trip Duration (minutes)'})
            st.plotly_chart(fig_duration)
        except Exception as e:
            st.error(f"Error creating duration distribution plot: {e}")

        # Plot: Passenger Count Distribution
        st.subheader("Passenger Count Distribution")
        try:
            fig_passenger = px.histogram(df, x='passenger_count', nbins=10, title='Passenger Count Distribution', labels={'passenger_count':'Number of Passengers'})
            st.plotly_chart(fig_passenger)
        except Exception as e:
            st.error(f"Error creating passenger count distribution plot: {e}")

        # Plot: Average Trip Duration by Passenger Count
        st.subheader("Average Trip Duration by Passenger Count")
        try:
            avg_duration = df.groupby('passenger_count')['duration'].mean().reset_index()
            fig_avg_duration = px.bar(avg_duration, x='passenger_count', y='duration', title='Average Trip Duration by Passenger Count', labels={'duration':'Average Duration (minutes)', 'passenger_count':'Number of Passengers'})
            st.plotly_chart(fig_avg_duration)
        except Exception as e:
            st.error(f"Error creating average duration by passenger count plot: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
