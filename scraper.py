import os
  import random
  import json
  import logging
  import pandas as pd
  import time
  from datetime import datetime
  from selenium import webdriver
  from selenium.webdriver.firefox.service import Service
  from selenium.webdriver.firefox.options import Options
  from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
  from webdriver_manager.firefox import GeckoDriverManager
  
  # Setup logging
  logging.basicConfig(
      filename="logs/scraper.log",
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s"
  )
  
  def scrape():
      try:
          logging.info("🔄 Starting Redfin Scraper...")
          
          # Define a list of User-Agents to rotate
          USER_AGENTS = [
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
              "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0",
          ]
  
          # OPTIONAL - Update with your actual Firefox profile path
          profile_path = "/home/your_name/.mozilla/firefox/abcdefgh.your-profile"
  
          # Setup Firefox options for stealth mode
          options = Options()
          options.profile = FirefoxProfile(profile_path) # OPTIONAL
          options.add_argument("--headless")
          options.add_argument("--disable-gpu")
          options.set_preference("dom.webdriver.enabled", False)
          options.set_preference("useAutomationExtension", False)
  
          # Randomly select a User-Agent
          user_agent = random.choice(USER_AGENTS)
          options.set_preference("general.useragent.override", user_agent)
  
          # Use WebDriver Manager to install Geckodriver
          service = Service(GeckoDriverManager().install())
          driver = webdriver.Firefox(service=service, options=options)
  
          # Redfin search URL
          base_url = "https://www.redfin.com/neighborhood/547223/CA/Los-Angeles/Hollywood-Hills"
          scraped_data = []
          today = datetime.today().strftime("%Y-%m-%d")
  
          driver.get(base_url)
          time.sleep(random.uniform(5, 8))  # Random delay
          
          # Scraping logic (Extracting listings and saving data) from Part 1 
          #...
  
          df = pd.DataFrame(scraped_data)
          df["Date"] = today  # Add date for historical tracking
  
          # Save daily CSV
          daily_filename = f"data/redfin_hollywood_hills_{today}.csv"
          df.to_csv(daily_filename, index=False)
          logging.info(f"Saved daily data: {daily_filename}")
  
          # Append to master dataset
          master_filename = "data/redfin_hollywood_hills_master.csv"
          if os.path.exists(master_filename):
              master_df = pd.read_csv(master_filename)
              df = pd.concat([master_df, df]).drop_duplicates(subset=["Address", "Date"])
          df.to_csv(master_filename, index=False)
          logging.info(f"Updated master dataset: {master_filename}")
  
          driver.quit()
          exit(0)  # Exit successfully
  
      except Exception as e:
          logging.error(f"❌ Scraper failed: {e}")
          exit(1)  # Exit with failure
  
  if __name__ == "__main__":
      scrape()
  
