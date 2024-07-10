import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Base URL of the page to scrape
base_url = "https://www2.eecs.berkeley.edu/Faculty/Lists/EE/faculty.html"

# Function to extract details from a faculty profile page
def extract_profile_details(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all faculty divs
    faculty_divs = soup.find_all('div', class_='cc-image-list__item__content')
    if not faculty_divs:
        raise ValueError("No faculty information found on the page.")

    faculty_data = []

    for faculty_div in faculty_divs:
        try:
            name = faculty_div.h3.a.text.strip()
            position = faculty_div.find('strong').text.strip()

            # Extracting the email
            email_line = faculty_div.find('p').find('br').next_sibling.strip()
            email = email_line.split(';')[1].strip().split(',')[0].strip()

            # Extract research focus
            research_focus_elems = faculty_div.find('p').find_all('a')
            research_focus = '; '.join([elem.text for elem in research_focus_elems])

            faculty_data.append({
                'University': 'Berkeley',
                'Department': 'Electrical Engineering',
                'Name': name,
                'Position': position,
                'Link': base_url,
                'Email': email,
                'Research Focus': research_focus
            })
        except AttributeError:
            continue  # Skip if any information is missing for a faculty member
        except IndexError:
            continue  # Skip if email extraction fails

    return faculty_data

# Scrape faculty profile details
data = extract_profile_details(base_url)

# Define the CSV file name and path (adjust as needed)

csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\4_Berkeley\Berkeley_ElectricalEngineering.csv'

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email', 'Research Focus']

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been saved to {csv_file}.")
