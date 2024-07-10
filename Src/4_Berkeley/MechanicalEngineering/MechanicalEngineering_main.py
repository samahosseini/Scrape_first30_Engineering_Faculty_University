import csv
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def fetch_urls_from_page(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all span tags with class 'field--name-title'
        span_tags = soup.find_all('span', class_='field--name-title')

        extracted_urls = []

        for span_tag in span_tags:
            # Find the parent <a> tag
            anchor_tag = span_tag.parent

            if anchor_tag and anchor_tag.name == 'a' and anchor_tag.has_attr(
                    'href'):
                href_attr = anchor_tag['href']

                # Check if href_attr starts with '/faculty/'
                if href_attr.startswith('/faculty/'):
                    extracted_urls.append(
                        href_attr.strip())  # Append the extracted URL path

        return extracted_urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def scrape_person_info(url):
    # Initialize an empty dictionary to store the scraped data
    person_info = {
        'University': 'Berkeley',
        'Department': 'Mechanical Engineering',
        'Link': url,
        'Research Focus': ''
    }

    # Send a request to fetch the HTML content of the page
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the name
    name_tag = soup.find('h1', class_='title')
    name = name_tag.text.strip() if name_tag else "Name not found"
    person_info['Name'] = name

    # Extract the title
    position_div = soup.find('div', class_='field-name-field-openberkeley-person-title')
    position = position_div.find('div', class_='field-item').text.strip() if position_div else "Title not found"
    person_info['Position'] = position

    # Extract the department
    department_div = soup.find('div', class_='field-name-field-openberkeley-person-dept')
    department = department_div.find('div', class_='field-item').text.strip() if department_div else "Department not found"
    person_info['Department'] = department

    # Extract research interests
    research_div = soup.find('div', class_='field-name-field-openberkeley-person-resint')
    if research_div:
        research_interests = research_div.find('div', class_='field-item').text.strip()
        person_info['Research Focus'] = research_interests

    # Extract email
    email_div = soup.find('div', class_='field-name-field-openberkeley-person-email')
    if email_div:
        email_a = email_div.find('a')
        if email_a and email_a.has_attr('href') and email_a['href'].startswith('mailto:'):
            email = email_a['href'][7:]  # Extract email address after 'mailto:'
        else:
            email = "Email not found"
        person_info['Email'] = email
    else:
        person_info['Email'] = "Email not found"

    return person_info

# Base URL of the directory page
base_url = "https://vcresearch.berkeley.edu/faculty-expertise"

# Fetch URLs from the directory page
links = fetch_urls_from_page(base_url)

# Extract details from each profile and prepare the data for CSV
data = []
for link in links:
    profile = scrape_person_info(link)
    data.append(profile)

# Define the CSV file path csv_file =
# r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\4_Berkeley
# \Berkeley_MechanicalEngineering.csv"
csv_file = "me.csv"

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email',
           'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
