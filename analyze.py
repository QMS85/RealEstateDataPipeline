import os
  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
  import seaborn as sns
  import logging
  from datetime import datetime
  
  # Setup logging
  logging.basicConfig(
      filename="logs/analyze.log",
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s"
  )
  
  # Load dataset (specific date or full historical dataset)
  def load_data(date=None):
      if date:
          file_path = f"data/redfin_hollywood_hills_{date}.csv"
      else:
          file_path = "data/redfin_hollywood_hills_master.csv"
  
      if os.path.exists(file_path):
          df = pd.read_csv(file_path)
          df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
          logging.info(f"📊 Loaded data from {file_path}")
          return df
      else:
          logging.warning(f"⚠️ No data found for {date or 'historical records'}!")
          return pd.DataFrame()
  
  # Handle missing values & clean data
  def clean_data(df):
      logging.info("🛠 Cleaning Data...")
  
      # Replace invalid values
      df.replace({"—": np.nan, "N/A": np.nan, "": np.nan}, inplace=True)
  
      # Convert numeric columns
      df["Price"] = df["Price"].str.replace("[$,]", "", regex=True).astype(float)
      df["SqFt"] = df["SqFt"].str.replace(",", "", regex=True).astype(float)
      df["Beds"] = df["Beds"].str.extract("(\d+)").astype(float)
      df["Baths"] = df["Baths"].str.extract("(\d+)").astype(float)
  
      # Convert Latitude & Longitude to float
      df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
      df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
  
      # Drop rows missing essential values
      df.dropna(subset=["Price", "Beds", "Baths", "SqFt", "Latitude", "Longitude"], inplace=True)
  
      logging.info(f"✅ Cleaned data: {len(df)} valid listings remaining.")
      return df
  
  # Generate summary statistics
  def summarize_data(df):
      summary = df.describe()
      logging.info(f"\n📊 Summary Statistics:\n{summary}")
  
  # Plot price trends over time
  def plot_price_trend(df):
      plt.figure(figsize=(12, 6))
      sns.lineplot(x="Date", y="Price", data=df, estimator="mean", ci=None)
      plt.title("📈 Average Listing Price Over Time")
      plt.xlabel("Date")
      plt.ylabel("Average Price ($)")
      plt.xticks(rotation=45)
      plt.grid()
      plt.savefig("plots/price_trend.png")
      logging.info("📊 Saved price trend plot.")
  
  # Show the number of listings over time
  def plot_listings_trend(df):
      plt.figure(figsize=(12, 6))
      df.groupby("Date").size().plot(kind="line", marker="o")
      plt.title("📉 Number of Listings Over Time")
      plt.xlabel("Date")
      plt.ylabel("Listings Count")
      plt.xticks(rotation=45)
      plt.grid()
      plt.savefig("plots/listings_trend.png")
      logging.info("📊 Saved listings trend plot.")
  
  # Show top & bottom listings
  def show_extreme_listings(df):
      logging.info("\n💰 Top 5 Most Expensive Listings:")
      logging.info(df.nlargest(5, "Price").to_string())
  
      logging.info("\n💸 Top 5 Cheapest Listings:")
      logging.info(df.nsmallest(5, "Price").to_string())
  
  # Save cleaned data & append to master dataset
  def save_cleaned_data(df, date):
      cleaned_filename = f"data/redfin_hollywood_hills_cleaned_{date}.csv"
      df.to_csv(cleaned_filename, index=False)
      logging.info(f"✅ Saved cleaned daily data: {cleaned_filename}")
  
      # Append to master dataset
      master_filename = "data/redfin_hollywood_hills_master_cleaned.csv"
      if os.path.exists(master_filename):
          master_df = pd.read_csv(master_filename)
          df = pd.concat([master_df, df]).drop_duplicates(subset=["Address", "Date"])
  
      df.to_csv(master_filename, index=False)
      logging.info(f"✅ Updated master dataset: {master_filename}")
  
  # Run analysis
  def run_analysis(date=None):
      try:
          logging.info(f"\n🚀 Running Analysis for {date or 'historical data'}...\n")
          df = load_data(date)
  
          if df.empty:
              logging.warning("⚠️ No data available to analyze.")
              return False
  
          df = clean_data(df)
          summarize_data(df)
  
          if date:
              save_cleaned_data(df, date)
  
          if not date:
              plot_price_trend(df)
              plot_listings_trend(df)
  
          show_extreme_listings(df)
          logging.info("✅ Analysis complete.\n")
          return True
  
      except Exception as e:
          logging.error(f"❌ Analysis failed: {e}")
          return False
  
  # Run the script automatically
  if __name__ == "__main__":
      today = datetime.today().strftime("%Y-%m-%d")
      run_analysis(today)  # Run for today’s data
      run_analysis()       # Run historical analysis
  
