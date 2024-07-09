import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape the data from the given URL
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the name
        name_div = soup.find('div', id='gt-page-title')
        if name_div and name_div.find('span'):
            name = name_div.find('span').text.strip()
        else:
            name = 'Not found'

        # Extracting the position
        position_elem = soup.find('h6', class_='card-block__subtitle')
        if position_elem:
            position = position_elem.text.strip()
        else:
            position = 'Not found'

        # Extracting the email
        email_elem = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
        if email_elem:
            email = email_elem.text.strip()
        else:
            email = 'Not found'

        # Extracting the research focus
        research_focus_elem = soup.find('strong', text='Research Areas:')
        if research_focus_elem:
            research_focus = research_focus_elem.parent.text.split('Research Areas:')[1].strip()
        else:
            research_focus = 'Not found'

        # Extract the department names
        school_elem = soup.select_one(
            '.block-field-blocknodecoc-personfield-person-school .field__item a')
        center_elem = soup.select_one(
            '.block-field-blocknodecoc-personfield-person-center .field__item a')

        if school_elem and center_elem:
            school = school_elem.text.strip()
            center = center_elem.text.strip()
            # Concatenate the department names
            department = f"{school}, {center}"
        else:
            department = 'Computing Engineering'

        return name, position, email, research_focus, department
    else:
        return 'Not found', 'Not found', 'Not found', 'Not found'

# Path to the CSV file
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\ComputingEngineering\profiles_urls.csv'

# Read the CSV file
df = pd.read_csv(csv_file)
# df = df.head(10)

# Initialize new columns in the DataFrame
df['Name'] = ''
df['Position'] = ''
df['Email'] = ''
df['Research Focus'] = ''

# Loop through URLs and scrape data
for index, row in df.iterrows():
    url = row['Link']  # Assuming the column containing URLs is named 'URL'
    name, position, email, research_focus, department = scrape_data(url)
    df.at[index, 'Name'] = name
    df.at[index, 'Position'] = position
    df.at[index, 'Email'] = email
    df.at[index, 'Research Focus'] = research_focus
    df.at[index, 'Department'] = department

# Save the updated DataFrame back to the CSV
csv_file_result = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\3_GeorgiaTech\ComputingEngineering.csv'
df.to_csv(csv_file_result, index=False)

print("Scraping and CSV update complete.")
