import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


def fetch_urls_from_page(url):
    profiles = []
    page_number = 0

    while True:
        try:
            # Send a GET request to the URL
            response = requests.get(url, params={'page': page_number})
            response.raise_for_status()  # Raise an exception for HTTP errors

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all span tags with class 'field--name-title'
                span_tags = soup.find_all('span', class_='field--name-title')

                for span_tag in span_tags:
                    # Initialize profile dictionary
                    profile = {
                        'University': 'Berkeley',
                        'Department': 'N/A',
                        'Name': span_tag.text.strip(),
                        'Position': 'N/A',
                        'Link': 'N/A',
                        'Email': 'N/A',
                        'Research Focus': 'N/A'
                    }

                    # Find the parent <a> tag
                    anchor_tag = span_tag.parent

                    if anchor_tag and anchor_tag.name == 'a' and anchor_tag.has_attr(
                            'href'):
                        href_attr = anchor_tag['href']

                        # Check if href_attr starts with '/faculty/'
                        if href_attr.startswith('/faculty/'):
                            profile['Link'] = urljoin(url, href_attr)

                    # Find the department
                    department_div = span_tag.find_parent('article').find('div',
                                                                          class_='field--name-field-department')
                    if department_div:
                        department_link = department_div.find('a')
                        if department_link:
                            profile['Department'] = department_link.text.strip()

                    profiles.append(profile)

                # Check for "Load More" button
                pager = soup.find('ul', class_='js-pager__items pager')
                if pager and pager.find('a', class_='button', rel='next'):
                    page_number += 1  # Increment the page number to fetch the next page
                else:
                    break  # No more pages to load, exit the loop

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            break

    return profiles


# Example usage:
directory_url = "https://vcresearch.berkeley.edu/faculty-expertise"
all_profiles = fetch_urls_from_page(directory_url)

# Define the CSV file path
csv_file = "profiles_urls.csv"

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_profiles)

print(f"Data has been saved to {csv_file}.")
