import streamlit as st
  import pandas as pd
  import matplotlib.pyplot as plt
  import matplotlib.ticker as mtick
  from matplotlib.ticker import FuncFormatter
  import seaborn as sns
  import folium
  from streamlit_folium import st_folium
  import numpy as np
  import glob
  import os
  import re
  
  # Fetch available dates from stored CSV files
  def get_available_dates():
      files = glob.glob("data/redfin_hollywood_hills_*.csv")
      
      # Extract valid dates from filenames (YYYY-MM-DD format)
      date_pattern = re.compile(r"redfin_hollywood_hills_(\d{4}-\d{2}-\d{2})\.csv")
      dates = sorted(
          {date_pattern.search(f).group(1) for f in files if date_pattern.search(f)},
          reverse=True
      )
      return dates
  
  # Load selected date's data
  @st.cache_data
  def load_data(selected_date=None):
      if not selected_date:
          st.error("❌ No date selected.")
          return pd.DataFrame()
      
      file_path = f"data/redfin_hollywood_hills_cleaned_{selected_date}.csv"
      if not os.path.exists(file_path):
          st.error(f"❌ Cleaned data file not found: {file_path}")
          return pd.DataFrame()
  
      try:
          df = pd.read_csv(file_path)
  
          # 🛠 Handle missing values & clean numeric columns
          df.replace({'—': np.nan, 'N/A': np.nan, '': np.nan}, inplace=True)
          
          df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
          df["Beds"] = pd.to_numeric(df["Beds"], errors="coerce")
          df["Baths"] = pd.to_numeric(df["Baths"], errors="coerce")
          df["SqFt"] = pd.to_numeric(df["SqFt"], errors="coerce")
          df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
          df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
  
          df.dropna(subset=["Price", "Beds", "Baths", "SqFt", "Latitude", "Longitude"], inplace=True)
  
          return df
  
      except FileNotFoundError:
          st.error(f"❌ Data file not found: {file_path}")
          return pd.DataFrame()
  
  # Load historical dataset
  @st.cache_data
  def load_historical_data():
      master_file = "data/redfin_hollywood_hills_master_cleaned.csv"
      try:
          df = pd.read_csv(master_file)
          
          df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
          df["Beds"] = pd.to_numeric(df["Beds"], errors="coerce")
          df["Baths"] = pd.to_numeric(df["Baths"], errors="coerce")
          df["SqFt"] = pd.to_numeric(df["SqFt"], errors="coerce")
          df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
          
          df.dropna(subset=["Price", "Beds", "Baths", "SqFt", "Date"], inplace=True)
  
          return df
  
      except FileNotFoundError:
          st.error(f"❌ Historical data file not found.")
          return pd.DataFrame()
  
  # Streamlit UI
  st.title("🏡 Hollywood Hills Real Estate Dashboard")
  st.write("Analyze real estate trends in Hollywood Hills using interactive visualizations.")
  
  # Create Tabs
  tab1, tab2 = st.tabs(["📆 Listings by Date", "📈 Historical Trends"])
  
  # TAB 1: Listings by Date
  with tab1:
      st.subheader("📆 View Listings by Date")
  
      # Dropdown to select a date
      available_dates = get_available_dates()
      selected_date = st.selectbox("Select Date", available_dates)
  
      # Load selected day's data
      df = load_data(selected_date)
  
      if df.empty:
          st.warning("⚠️ No data available for the selected date.")
          st.stop()
  
      # Sidebar Filters
      st.sidebar.header("🔍 Filter Listings")
  
      show_all = st.sidebar.checkbox("Show All Properties", value=False)
  
      if show_all:
          filtered_df = df
      else:
          min_price, max_price = df["Price"].min(), df["Price"].max()
          selected_price = st.sidebar.slider("Select Price Range ($)", min_value=int(min_price), max_value=int(max_price), value=(int(min_price), int(max_price)))
  
          filtered_df = df[(df["Price"] >= selected_price[0]) & (df["Price"] <= selected_price[1])]
  
      st.subheader(f"📊 {len(filtered_df)} Listings Found")
      
      # Display Listings
      st.dataframe(filtered_df[["Price", "Beds", "Baths", "SqFt", "Address", "Link"]])
  
      # Price Distribution
      st.subheader("💰 Price Distribution")
      fig, ax = plt.subplots(figsize=(8, 4))
      sns.histplot(filtered_df["Price"], bins=30, kde=True, ax=ax)
      ax.set_xlabel("Price ($)")
      ax.set_ylabel("Count")
      st.pyplot(fig)
  
      # Property Locations Map
      st.subheader("📍 Property Locations")
      m = folium.Map(location=[34.1, -118.3], zoom_start=12)
  
      for _, row in filtered_df.iterrows():
          folium.Marker(
              location=[row["Latitude"], row["Longitude"]],
              popup=f"{row['Address']} - ${row['Price']:,.0f}",
              icon=folium.Icon(color="blue", icon="home"),
          ).add_to(m)
  
      st_folium(m, width=800, height=500)
  
  # TAB 2: Historical Trends
  with tab2:
      st.subheader("📈 Historical Trends")
  
      historical_df = load_historical_data()
      if historical_df.empty:
          st.warning("⚠️ No historical data available.")
          st.stop()
  
      # Select Date Range
      min_date, max_date = historical_df["Date"].min().date(), historical_df["Date"].max().date()
      selected_range = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="YYYY-MM-DD")
  
      # Filter data
      filtered_historical_df = historical_df[
          (historical_df["Date"] >= pd.to_datetime(selected_range[0])) &
          (historical_df["Date"] <= pd.to_datetime(selected_range[1]))
      ]
  
      # Average Price Over Time
      st.subheader("📊 Average Price Over Time")
      fig, ax = plt.subplots(figsize=(10, 5))
      filtered_historical_df.groupby("Date")["Price"].mean().plot(ax=ax, marker="o")
      ax.set_xlabel("Date")
      ax.set_ylabel("Average Price ($)")
      st.pyplot(fig)
  
      # Number of Listings Over Time
      st.subheader("🏠 Number of Listings Over Time")
      fig, ax = plt.subplots(figsize=(10, 5))
      filtered_historical_df.groupby("Date")["Address"].count().plot(ax=ax, marker="o", color="red")
      ax.set_xlabel("Date")
      ax.set_ylabel("Listings Count")
      st.pyplot(fig)
  
      st.subheader(f"📊 Summary for {selected_range[0]} to {selected_range[1]}")
      st.write(filtered_historical_df.describe())
  
  st.write("Data Source: Redfin Scraper")
