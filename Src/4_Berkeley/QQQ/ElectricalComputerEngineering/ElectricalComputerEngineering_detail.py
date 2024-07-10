import pandas as pd
import requests
from bs4 import BeautifulSoup


# Function to scrape the data from the given URL using requests and BeautifulSoup
def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the name
    name_div = soup.find('div', id='gt-page-title')
    name = name_div.find('h1',
                         class_='page-title').span.text.strip() if name_div else 'Not found'

    # Extract the position
    position_div = soup.find('div',
                             class_='field--name-field-person-official-job-title')
    position = position_div.find('div',
                                 class_='field__item').text.strip() if position_div else 'Not found'

    # Extract the email
    email_elem = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
    email = email_elem.text.strip() if email_elem else 'Not found'

    # Extract the research focus
    research_div = soup.find('div', class_='field--name-field-person-research')
    if research_div:
        research_focus_ul = research_div.find('ul')
        research_focus = ', '.join([li.text.strip() for li in
                                    research_focus_ul.find_all(
                                        'li')]) if research_focus_ul else 'Not found'
    else:
        research_focus = 'Not found'

    # Extract the department names
    school_elem = soup.select_one(
        '.block-field-blocknodecoc-personfield-person-school .field__item a')
    center_elem = soup.select_one(
        '.block-field-blocknodecoc-personfield-person-center .field__item a')
    department = 'Electrical and Computer Engineering'
    if school_elem and center_elem:
        school = school_elem.text.strip()
        center = center_elem.text.strip()
        department = f"{school}, {center}"

    return {
        "Name": name,
        "Position": position,
        "Email": email,
        "Research Focus": research_focus,
        "Department": department
    }


# Path to the CSV file (considering the use of raw string for the path)
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\ElectricalComputerEngineering\profiles_urls.csv'

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
output_csv_file = 'xxx.csv'
df.to_csv(output_csv_file, index=False)

print("Scraping and CSV update complete.")
