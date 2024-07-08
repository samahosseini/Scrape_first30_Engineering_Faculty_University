import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the page to scrape
base_url = "https://www.cc.gatech.edu/people/faculty"


# Function to get links from a single page
def get_links_from_page(url):
    links = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        h4_tags = soup.find_all('h4', class_='card-block__title')
        for h4 in h4_tags:
            a_tag = h4.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href = a_tag['href']
                if href.startswith('/'):
                    full_url = f"https://www.cc.gatech.edu{href}"
                else:
                    full_url = href
                links.append(full_url)
    else:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")
    return links


# Main function to iterate through pages
def scrape_all_links():
    page_number = 0
    all_links = []

    while True:
        page_url = f"{base_url}?page={page_number}"
        print(f"Scraping page {page_number}: {page_url}")
        links = get_links_from_page(page_url)
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
        'Department': 'Computing Engineering',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': link,
        'Email': 'N/A',
        'Research Focus': 'N/A'
    }
    data.append(profile)

# Define the CSV file name
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\ComputingEngineering\profiles_urls.csv'

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
