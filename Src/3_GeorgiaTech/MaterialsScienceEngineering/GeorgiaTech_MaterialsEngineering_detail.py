import os
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Function to scrape the data from the given URL using requests and
# BeautifulSoup
def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the name
    name_div = soup.find('div', id='nametitle')
    first_name = name_div.find('div',
                               class_='field--name-field-first-name').text.strip() if name_div.find(
        'div', class_='field--name-field-first-name') else ''
    last_name = name_div.find('div',
                              class_='field--name-field-last-name').text.strip() if name_div.find(
        'div', class_='field--name-field-last-name') else ''
    name = f"{first_name} {last_name}" if first_name and last_name else 'Not found'

    # Extract the position
    position_div = soup.find('div', class_='field__items')
    position_tag = position_div.find('div', class_='field__item',
                                     recursive=False)
    position = position_tag.text.strip() if position_tag else 'Not found'

    # Extract the email
    email_tag = soup.find('a', href=lambda href: href and "mailto" in href)
    email = email_tag.text.strip() if email_tag else 'Not found'

    # Extract the research focus
    research_focus = []
    research_tags = soup.find_all('div', class_='field__item')
    for tag in research_tags:
        a_tag = tag.find('a', href=True)
        if a_tag:
            href = a_tag['href']
            if "/research-area/" in href:
                research_focus.append(tag.text.strip())

    if not research_focus:
        research_focus = 'Not found'
    else:
        research_focus = ', '.join(research_focus)

    university = 'GeorgiaTech'
    department = 'Material Science Engineering'

    return {
        "Name": name,
        "Position": position,
        "Email": email,
        "Research Focus": research_focus,
        "Department": department
    }


# Path to the CSV file (considering the use of raw string for the path)
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\MaterialsScienceEngineering\x.csv'

# Read the CSV file
df = pd.read_csv(csv_file)

# Initialize new columns in the DataFrame
df['Name'] = ''
df['Position'] = ''
df['Email'] = ''
df['Research Focus'] = ''
df['University'] = 'GeorgiaTech'
df['Department'] = 'Material Science Engineering'

# Loop through URLs and scrape data
for index, row in df.iterrows():
    url = row['Link']  # Assuming the column containing URLs is named 'Link'
    scraped_data = scrape_data(url)
    df.at[index, 'Name'] = scraped_data["Name"]
    df.at[index, 'Position'] = scraped_data["Position"]
    df.at[index, 'Email'] = scraped_data["Email"]
    df.at[index, 'Research Focus'] = scraped_data["Research Focus"]

# Define the output CSV file path
output_csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\3_GeorgiaTech\GeorgiaTech_MaterialScience.csv'

# Specify the headers/column names
headers = ['University', 'Department', 'Name', 'Position', 'Link', 'Email', 'Research Focus']

# Write data to CSV
df.to_csv(output_csv_file, index=False, columns=headers)

print(f"Scraping and CSV update complete. Data saved to {output_csv_file}.")
