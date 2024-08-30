
# Terrorist Activity Scraper

## Overview

This project is a Python-based web scraper designed to extract and compile terrorist activity data from the South Asia Terrorism Portal (SATP) for the year 2024. The data is collected monthly and saved into a CSV file. The scraper is scheduled to run twice daily at 6 AM and 6 PM to ensure the data is up-to-date.

## Prerequisites

Before running the scraper, ensure you have the following installed on your system:

- Python 3.x
- `pip` (Python package installer)
- Google Chrome browser
- Chrome WebDriver (compatible with your Chrome version)

## Python Libraries

The following Python libraries are required:

- `selenium`
- `beautifulsoup4`
- `pandas`
- `schedule`

You can install the required libraries using the following command:

```bash
pip install selenium beautifulsoup4 pandas schedule
```

## Usage

1. **Setup ChromeDriver**: Download the Chrome WebDriver and place it in a directory that is in your system's PATH or specify its location in the `webdriver.Chrome()` initialization.

2. **Run the Scraper**: Execute the Python script to start the scraping process.

```bash
python scrape_data.py
```

3. **Automated Scheduling**: The scraper is set to run automatically at 6 AM and 6 PM every day. This is handled using the `schedule` library.

4. **Output**: The data will be saved into a CSV file named `terrorist_activity_2024_full.csv` in the same directory where the script is executed.

## Script Details

### `scrape_data()`

- Initializes the Selenium WebDriver for Chrome.
- Iterates through a list of URLs, each corresponding to a month's terrorist activities in 2024.
- Waits for the table containing the data to load, then extracts the data using BeautifulSoup.
- Cleans up the extracted data and appends it to a list.
- Converts the list into a Pandas DataFrame and saves it as `terrorist_activity_2024_full.csv`.

### Scheduling

The scraper is scheduled to run at 6:00 AM and 6:00 PM every day using the `schedule` library. The script runs continuously, checking for scheduled tasks every hour.

## Notes

- **WebDriver Wait**: The script waits up to 10 seconds for the page content (specifically the table) to load before attempting to extract data.
- **Error Handling**: If a table is not found on a page, the script will skip to the next URL.
- **Data Cleaning**: The script removes unnecessary links and text ("read more", "read less") from the incident descriptions.

## Troubleshooting

- **WebDriver Compatibility**: Ensure your Chrome WebDriver version matches your installed Chrome browser version.
- **Internet Connection**: A stable internet connection is required for the script to access the SATP website.
- **Running in Background**: If you want the script to run continuously in the background, consider using a process manager like `pm2` or running it inside a `screen` session.

## License

This project is licensed under the MIT License.
