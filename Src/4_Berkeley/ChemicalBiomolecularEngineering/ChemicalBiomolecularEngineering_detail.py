import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape the data from the given URL using requests and BeautifulSoup
def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the name
    name = soup.find('h1', class_='page-title').text.strip() if soup.find('h1', class_='page-title') else 'Not found'

    # Extract the position
    position_tag = soup.find('div', class_='field--name-field-person-job-title-s-')
    position = position_tag.find('div', class_='field__item').text.strip() if position_tag else 'Not found'

    # Extract the email
    email_tag = soup.find('div', class_='field--name-field-person-email')
    email = email_tag.find('a').text.strip() if email_tag else 'Not found'

    # Extract the research focus
    research_focus_tag = soup.find('div', class_='field__label h4', text='Disciplines')
    if research_focus_tag:
        research_focus_items = research_focus_tag.find_next_sibling('div').find_all('div', class_='field__item')
        research_focus = ", ".join([item.text.strip() for item in research_focus_items])
    else:
        research_focus = 'Not found'

    department = 'Chemical and Biomolecular Engineering'

    return {
        "Name": name,
        "Position": position,
        "Email": email,
        "Research Focus": research_focus,
        "Department": department
    }

# Path to the CSV file (considering the use of raw string for the path)
csv_file = r'/Src/4_Berkeley/ChemicalBiomolecularEngineering/profiles_urls.csv'

# Read the CSV file
df = pd.read_csv(csv_file)

# Initialize new columns in the DataFrame
df['Name'] = ''
df['Position'] = ''
df['Email'] = ''
df['Research Focus'] = ''
df['Department'] = ''

# Loop through URLs and scrape data
for index, row in df.iterrows():
    url = row['Link']  # Assuming the column containing URLs is named 'Link'
    scraped_data = scrape_data(url)
    df.at[index, 'Name'] = scraped_data["Name"]
    df.at[index, 'Position'] = scraped_data["Position"]
    df.at[index, 'Email'] = scraped_data["Email"]
    df.at[index, 'Research Focus'] = scraped_data["Research Focus"]
    df.at[index, 'Department'] = scraped_data["Department"]

# Save the updated DataFrame back to the CSV
output_csv_file = r'/Result/4_Berkeley/Berkeley_ChemicalBiomolecularEngineering.csv'
df.to_csv(output_csv_file, index=False)

print("Scraping and CSV update complete.")
