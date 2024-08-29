import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data():
    # setting up selenium webdriver for chrome
    driver = webdriver.Chrome()

    # urls to scrap
    urls = [
        "https://www.satp.org/terrorist-activity/india-Jan-2024",
        "https://www.satp.org/terrorist-activity/india-Feb-2024",
        "https://www.satp.org/terrorist-activity/india-Mar-2024",
        "https://www.satp.org/terrorist-activity/india-Apr-2024",
        "https://www.satp.org/terrorist-activity/india-May-2024",
        "https://www.satp.org/terrorist-activity/india-Jun-2024",
        "https://www.satp.org/terrorist-activity/india-Jul-2024",
        "https://www.satp.org/terrorist-activity/india-Aug-2024"
    ]

    data = []

    # iterating over each month
    for url in urls:
        # extracting the month from the URL
        month = url.split('-')[-2] + "-" + url.split('-')[-1]
        print(f"Processing URL: {url}")
        
        # read the URL
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
        )
        
        # getting the page source after the content has loaded
        page_source = driver.page_source
        
        # BeautifulSoup for parsing the content
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # extracting the table
        table = soup.find('table')
        if not table:
            print(f"No table found on the {month} page.")
            continue
        
        rows = table.find_all('tr')
        print(f"Found {len(rows)} rows in the table for {month}.")
        
        # skipping the header row
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 2:
                date = cells[0].text.strip()
                # extracting complete incident text, removing "read more" and "read less"
                incident_cell = cells[1]
                for elem in incident_cell.find_all(['a', 'span']):
                    elem.decompose()
                incident = incident_cell.get_text(strip=True, separator=' ')
                data.append([month, date, incident])

    # converting the list to a df
    if data:
        df = pd.DataFrame(data, columns=["Month", "Date", "Incident"])
        # save to csv
        df.to_csv('terrorist_activity_2024_full.csv', index=False)
        print("Data has been saved to terrorist_activity_2024_full.csv")
        print(f"Scraping completed at {time.strftime('%Y-%m-%d %H:%M:%S')} and saved to 'terrorist_activity_2024_full.csv'.")
    else:
        print("No data was found.")

    # close the browser
    driver.quit()

# scheduling the task to run at 6 AM and 6 PM every day
schedule.every().day.at("06:00").do(scrape_data)
schedule.every().day.at("18:00").do(scrape_data)

# running the scheduled tasks - check every hour for the scheduled task
while True:
    schedule.run_pending()
    time.sleep(3600)
