import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Base URL of the page to scrape
base_url = "https://www.isye.gatech.edu/people/faculty"


# Function to fetch URLs from the faculty page
def fetch_urls_from_page(url):
    links = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all <a> tags with href attributes
        a_tags = soup.find_all('a', href=True)

        for a_tag in a_tags:
            relative_url = a_tag['href']
            # Check if it's a faculty link
            if relative_url.startswith("/users/"):
                full_url = urljoin(base_url, relative_url)
                links.append(full_url)
    else:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")

    return links


# Fetch URLs from the faculty page
all_links = fetch_urls_from_page(base_url)

# Prepare the data for CSV
data = []
for link in all_links:
    profile = {
        'University': 'Georgia Tech',
        'Department': 'Industrial Systems Engineering',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': link,
        'Email': 'N/A',
        'Research Focus': 'N/A'
    }
    data.append(profile)

# Define the CSV file path
csv_file = "profiles_urls.csv"

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
