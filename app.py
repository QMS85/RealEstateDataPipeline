import streamlit as st
import pandas as pd
import os
from scraper import scrape

st.title("Redfin Hollywood Hills Scraper")

if st.button("Run Scraper"):
    with st.spinner("Scraping data..."):
        scrape()
    st.success("Scraping complete!")

# Show the latest data if available
data_dir = "data"
if os.path.exists(data_dir):
    files = [f for f in os.listdir(data_dir) if f.startswith("redfin_hollywood_hills_") and f.endswith(".csv")]
    if files:
        latest_file = sorted(files)[-1]
        df = pd.read_csv(os.path.join(data_dir, latest_file))
        st.subheader(f"Latest Data: {latest_file}")
        st.dataframe(df)
    else:
        st.info("No data files found yet.")
else:
    st.info("Data directory does not exist.")
