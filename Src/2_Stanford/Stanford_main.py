import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# URL to scrape
url = "https://engineering.stanford.edu/faculty-research/faculty"

# Initialize WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

def get_profiles_from_page(page_source):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all divs with the class 'field-content'
    divs_field_content = soup.find_all('div', class_='field-content')

    # Base URL for constructing the full URL
    base_url = "https://engineering.stanford.edu"

    # Initialize a list to store the profiles with URLs, names, and positions
    profiles = []

    # Iterate over each div to extract URLs, names, and positions
    for div in divs_field_content:
        # Extract the URL
        a_tag = div.find('a', href=True)
        if a_tag:
            relative_url = a_tag['href']
            full_url = f"{base_url}{relative_url}"

            # Extract the name
            name = div.get_text().strip()

            # Extract position for the profile URL
            position_div = div.find_next('div', class_='views-field views-field-su-person-short-title')
            if position_div:
                position_span = position_div.find('div', class_='field-content')
                if position_span:
                    position = position_span.get_text().strip()
                else:
                    position = "Position not found"
            else:
                position = "Position not found"

            # Append profile data with fixed values for specified columns
            profiles.append({
                'University': 'Stanford',
                'Department': 'Engineering',
                'Name': name,
                'Position': position,
                'Link': full_url,
                'Email': 'N/A',
                'Research Focus': 'N/A',
                'Profile_link': 'N/A'
            })

    return profiles

try:
    # Open the initial URL with WebDriver
    driver.get(url)

    all_profiles = []

    while True:
        # Get the current page source and extract profile URLs, names, and positions
        page_source = driver.page_source
        all_profiles.extend(get_profiles_from_page(page_source))

        try:
            # Wait for the "Load More People" button to be clickable
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'a.button.su-button.su-button--unstyled[rel="next"]'))
            )
            # Click the "Load More People" button
            load_more_button.click()
            # Wait for new content to load
            time.sleep(2)
        except Exception as e:
            # If no "Load More People" button is found, break the loop
            print("Load More button not found or not clickable:", e)
            break

finally:
    # Close the WebDriver
    driver.quit()

# Write the collected profiles to a CSV file
csv_file = "Primery_info.csv"
csv_columns = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
               'Research Focus', 'Profile_link']

try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for profile in all_profiles:
            writer.writerow(profile)
except IOError:
    print("I/O error")

print(f"{len(all_profiles)} profiles have been written to {csv_file}")
