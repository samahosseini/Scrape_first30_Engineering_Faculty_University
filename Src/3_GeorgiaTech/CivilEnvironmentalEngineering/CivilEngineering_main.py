import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Base URL of the page to scrape
base_url = "https://ce.gatech.edu/people"


# Function to get links from a single page
def fetch_urls_from_page(page_number):
    if page_number == 0:
        url = base_url
    else:
        url = f"{base_url}?page={page_number}"

    links = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all anchor tags with href attributes that match the pattern we're interested in
        anchors = soup.find_all('a', href=True)

        for anchor in anchors:
            relative_url = anchor['href']
            if relative_url.startswith(
                    '/directory'):  # Adjust this condition based on the pattern you expect
                full_url = urljoin(base_url, relative_url)
                links.append(full_url)
    else:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")

    return links


# Main function to iterate through pages
def scrape_all_links():
    page_number = 0
    all_links = []

    while page_number < 10:  # Loop through 10 pages (0 to 9)
        print(f"Scraping page {page_number}: {base_url}?page={page_number}")
        links = fetch_urls_from_page(page_number)
        if not links:
            break
        all_links.extend(links)
        page_number += 1

    return all_links


# Scrape all links
all_links = scrape_all_links()

# Preparing the data for CSV
data = []
for link in all_links:
    profile = {
        'University': 'GeorgiaTech',
        'Department': 'Civil and Environmental Engineering',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': link,
        'Email': 'N/A',
        'Research Focus': 'N/A'
    }
    data.append(profile)

# Define the CSV file name
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\CivilEnvironmentalEngineering\profiles_urls1.csv'

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
