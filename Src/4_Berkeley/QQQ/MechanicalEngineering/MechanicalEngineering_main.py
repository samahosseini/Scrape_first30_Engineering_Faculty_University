import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the faculty listing page
base_url = "https://www.me.gatech.edu/faculty"


# Function to fetch URLs from a single page
def fetch_urls_from_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all faculty__user-wrapper divs
    faculty_divs = soup.find_all('div', class_='faculty__user-wrapper')

    links = []
    base_url = "https://www.me.gatech.edu"

    for div in faculty_divs:
        a_tag = div.find('a', href=True)
        if a_tag:
            relative_url = a_tag['href']
            absolute_url = base_url + relative_url
            links.append(absolute_url)

    return links


# Function to fetch all URLs from all pages
def fetch_all_urls(base_url):
    all_links = []
    page_number = 0

    while True:
        page_url = f"{base_url}?page={page_number}"
        links = fetch_urls_from_page(page_url)

        if not links:  # Stop if no more links found
            break

        all_links.extend(links)
        page_number += 1

    return all_links


# Fetch all URLs from all pages
all_links = fetch_all_urls(base_url)

# Prepare the data for CSV
data = []
for link in all_links:
    profile = {
        'University': 'Georgia Tech',
        'Department': 'Mechanical Engineering',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': link,
        'Email': 'N/A',
        'Research Focus': 'N/A'
    }
    data.append(profile)

# Define the CSV file path
csv_file = "faculty_profiles.csv"

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
