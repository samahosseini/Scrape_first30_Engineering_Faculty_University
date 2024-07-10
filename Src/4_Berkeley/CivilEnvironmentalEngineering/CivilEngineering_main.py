import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Base URL of the page to scrape
base_url = "https://ce.berkeley.edu/people/faculty?type=faculty"


# Function to get faculty profile URLs from a single page
def fetch_urls_from_page(url):
    # if page_number == 0:
    #     url = base_url
    # else:
    #     url = f"{base_url}&type=faculty&page={page_number}"

    links = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        anchors = soup.find_all('a', href=True)

        for anchor in anchors:
            relative_url = anchor['href']
            if relative_url.startswith('/people/faculty/'):
                full_url = urljoin(base_url, relative_url)
                links.append(full_url)
    else:
        print(
            f"Failed to retrieve the page {url}. Status code: {response.status_code}")

    return links


# Function to extract details from a faculty profile page
def extract_profile_details(url):
    # response = requests.get(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        print(f"Failed to retrieve the profile page: {url}")
        return None
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract name
    name_tag = soup.find('h1', class_='page-header')
    name = name_tag.get_text(strip=True) if name_tag else 'N/A'

    # Extract position
    position = 'N/A'
    position_container = soup.find('div',
                                   class_='col-md-4 col-md-push-8 well text-center')
    if position_container:
        position_tag = position_container.find('span', class_='bold')
        if position_tag:
            position = position_tag.get_text(strip=True)

    # Extract research focus
    research_focus = 'N/A'
    research_focus_container = position_container.find('span', class_='h4',
                                                       text='Research Interests')
    if research_focus_container:
        research_focus_row = research_focus_container.find_next_sibling('div',
                                                                        class_='row')
        if research_focus_row:
            research_focus = research_focus_row.get_text(strip=True)

    # Extract email
    email_tag = soup.find('a', href=lambda href: href and 'mailto:' in href)
    email = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'

    return {
        'University': 'Berkeley',
        'Department': 'Civil and Environmental Engineering',
        'Name': name,
        'Position': position,
        'Link': url,
        'Email': email,
        'Research Focus': research_focus
    }


# Scrape faculty profile links from the first page

links = fetch_urls_from_page(base_url)

# Extract details from each profile and prepare the data for CSV
data = []
for link in links:
    profile = extract_profile_details(link)
    if profile:
        data.append(profile)

# Define the CSV file name and path (adjust as needed)
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\4_Berkeley\Berkeley_CivilEngineering.csv'

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
