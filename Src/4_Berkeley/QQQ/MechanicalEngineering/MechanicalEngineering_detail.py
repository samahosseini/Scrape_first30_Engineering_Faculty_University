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
    name = soup.find('h2', class_='display-4').text.strip() if soup.find('h2',
                                                                         class_='display-4') else 'Not found'

    # Extract the position
    position_tag = soup.find('div', class_='field--name-body').find('h4')
    position = position_tag.text.strip() if position_tag else 'Not found'

    # Extract the email
    email_tag = soup.find('a', href=lambda href: href and "mailto" in href)
    email = email_tag.text.strip() if email_tag else 'Not found'

    # Extract the research focus
    research_area_div = soup.find('div', class_='field__item')
    research_area_tag = research_area_div.find('h5')
    research_focus = research_area_tag.text.strip() if research_area_tag else 'Not found'

    university = 'GeorgiaTech'
    department = 'Mechanical Engineering'

    return {
        "University": university,
        "Department": department,
        "Name": name,
        "Position": position,
        "Email": email,
        "Research Focus": research_focus

    }


# Path to the CSV file containing URLs
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\MechanicalEngineering\faculty_profiles.csv'

# Read the CSV file
df = pd.read_csv(csv_file)

# Initialize new columns in the DataFrame
df['University'] = ''
df['Department'] = ''
df['Name'] = ''
df['Position'] = ''
df['Email'] = ''
df['Research Focus'] = ''

# Loop through URLs and scrape data
for index, row in df.iterrows():
    url = row['Link']  # Assuming the column containing URLs is named 'Link'
    scraped_data = scrape_data(url)
    df.at[index, 'Name'] = scraped_data["Name"]
    df.at[index, 'Position'] = scraped_data["Position"]
    df.at[index, 'Email'] = scraped_data["Email"]
    df.at[index, 'Research Focus'] = scraped_data["Research Focus"]
    df.at[index, 'Department'] = scraped_data["Department"]
    df.at[index, 'University'] = scraped_data["University"]

# Define the output CSV file path
output_csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\3_GeorgiaTech\GeorgiaTech_MechanicalEngineering.csv'

# Specify the headers/column names
headers = ['University', 'Department','Name', 'Position','Link',  'Email', 'Research Focus']

# Write data to CSV
df.to_csv(output_csv_file, index=False, columns=headers)

print(f"Scraping and CSV update complete. Data saved to {output_csv_file}.")
