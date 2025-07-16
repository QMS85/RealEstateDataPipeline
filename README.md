# Real Estate Data Pipeline Using Python

A Python-based data pipeline for scraping real estate listings and visualizing the results with a Streamlit web app.  
This is a free course, available on hackr.io which includes a certificate of completion.  
[Real Estate Data Pipeline Using Python](https://app.hackr.io/courses/python/data-pipeline)

---

## Features

- Automated scraping of Redfin listings using Selenium and Firefox WebDriver
- Rotating user agents for stealth scraping
- Daily and master CSV data storage
- Streamlit web interface to trigger scraping and view latest data

---

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/your-username/RealEstateDataPipeline.git
cd RealEstateDataPipeline
```

### 2. Install Python dependencies

It is recommended to use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

Install required libraries:

```sh
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install manually:

```sh
pip install selenium webdriver-manager pandas streamlit
```

---

## Required Libraries

- `selenium`
- `webdriver-manager`
- `pandas`
- `streamlit`

---

## Usage

### 1. Run the Scraper (Standalone)

You can run the scraper directly from the command line:

```sh
python scraper.py
```

This will save the scraped data to the `data/` directory.

### 2. Run the Streamlit App

Start the Streamlit web interface:

```sh
streamlit run app.py
```

- Click the **"Run Scraper"** button to trigger a new scrape.
- The latest data will be displayed in a table below.

---

## Deploying to Streamlit Cloud

1. Push your repository to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in.
3. Click **"New app"** and connect your GitHub repository.
4. Set the main file path to `app.py`.
5. (Optional) Add a `requirements.txt` file with the following content:

    ```
    selenium
    webdriver-manager
    pandas
    streamlit
    ```

6. Click **"Deploy"**.

**Note:**  
- Streamlit Cloud may not support browsers or Selenium WebDriver out of the box. For full scraping functionality, run locally or on a server with Firefox installed.
- For cloud deployment, consider using APIs or headless scraping services.

---

## Directory Structure

```
RealEstateDataPipeline/
├── app.py
├── scraper.py
├── data/
├── logs/
├── README.md
└── requirements.txt
```

---

## Troubleshooting

- **WebDriver errors:** Ensure Firefox is installed and accessible on your system.
- **Permission errors:** Make sure the `data/` and `logs/` directories are writable.
- **Streamlit Cloud limitations:** Selenium may not work on Streamlit Cloud due to browser/driver restrictions.

---

## License

MIT License

---

## Author

Your Name  
[Jonathan Peters](https://github.com/QMS85)
