from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Add headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
for key, value in headers.items():
    chrome_options.add_argument(f"--header={key}:{value}")

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL of the pages to scrape
base_url = "https://imes.mit.edu/people/faculty?page="

# Number of pages to scrape
num_pages = 4

# List to store all faculty data
faculty_data = []

# Iterate through each page
for page in range(num_pages):
    # Construct the URL
    url = base_url + str(page)
    driver.get(url)

    # Allow some time for the page to load
    driver.implicitly_wait(10)

    # Get the page source after rendering
    page_source = driver.page_source

    # Parsing the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all profiles
    profiles = soup.find_all("article", class_="node--profile--teaser")

    for profile in profiles:
        try:
            faculty_info = {}
            faculty_info['University'] = 'MIT'
            faculty_info['Department'] = 'Institute for Medical Engineering & Science'

            # Safely extract the necessary details
            try:
                name = profile.find("h2", class_="node--profile--teaser__title").text.strip()
                faculty_info['Name'] = name
            except AttributeError:
                faculty_info['Name'] = 'N/A'

            try:
                position = profile.find("div", class_="field--name-field-profile-position").text.strip()
                faculty_info['Position'] = position
            except AttributeError:
                faculty_info['Position'] = 'N/A'

            try:
                link = "https://imes.mit.edu" + profile.find("h2", class_="node--profile--teaser__title").find("a")["href"]
                faculty_info['Link'] = link
            except (AttributeError, TypeError):
                faculty_info['Link'] = 'N/A'

            # Extract email from mailto link within the profile context
            try:
                email_div = profile.find('div', class_="field--name-field-profile-email")
                email_tag = email_div.find('a', href=True)
                email = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'
                faculty_info['Email'] = email
            except (AttributeError, TypeError):
                faculty_info['Email'] = 'N/A'

            # Extract research focus areas
            try:
                research_focus_div = profile.find("div", class_="field--name-field-research-areas")
                research_focus_items = [item.text.strip() for item in research_focus_div.find_all("div", class_="field__item")]
                research_focus = ", ".join(research_focus_items)
                faculty_info['Research Focus'] = research_focus
            except AttributeError:
                faculty_info['Research Focus'] = 'N/A'

            # Append the information to the list
            faculty_data.append(faculty_info)

        except Exception as e:
            print(f"Error processing a faculty member block: {e}")


# Close the driver
driver.quit()

# Save the extracted data to a CSV file
file_path = '../../../../Result/1_MIT/IMES_Faculty.csv'
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = [
        'University',
        'Department',
        'Name',
        'Position',
        'Link',
        'Email',
        'Research Focus',
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(faculty_data)

print(f"Data saved to {file_path}")
