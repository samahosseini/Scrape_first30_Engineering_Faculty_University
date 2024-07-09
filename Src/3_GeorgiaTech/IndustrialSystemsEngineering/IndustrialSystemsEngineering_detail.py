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
    name = soup.find('h1', class_='page-title').text.strip() if soup.find('h1',
                                                                          class_='page-title') else 'Not found'

    # Extract the position
    position = soup.find('h2', class_='h3 mb-0').text.strip().replace('\n',
                                                                      ' ') if soup.find(
        'h2', class_='h3 mb-0') else 'Not found'

    # Extract the research focus
    expertise_div = soup.find('div', class_='ieuser-expertise')
    research_focus = ', '.join(item.text.strip() for item in
                               expertise_div.find_all(
                                   'li')) if expertise_div else 'Not found'

    # Assuming department information is not needed as it is hardcoded in the original script
    department = 'Electrical and Computer Engineering'

    return {
        "Name": name,
        "Position": position,
        "Research Focus": research_focus,
        "Department": department
    }


# Path to the CSV file (considering the use of raw string for the path)
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\IndustrialSystemsEngineering\profiles_urls.csv'

# Read the CSV file
df = pd.read_csv(csv_file)

# Initialize new columns in the DataFrame
df['Name'] = ''
df['Position'] = ''
df['Research Focus'] = ''
df['Department'] = ''

# Loop through URLs and scrape data
for index, row in df.iterrows():
    url = row['Link']  # Assuming the column containing URLs is named 'Link'
    scraped_data = scrape_data(url)
    df.at[index, 'Name'] = scraped_data["Name"]
    df.at[index, 'Position'] = scraped_data["Position"]
    df.at[index, 'Research Focus'] = scraped_data["Research Focus"]
    df.at[index, 'Department'] = scraped_data["Department"]

# Save the updated DataFrame back to the CSV
output_csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\3_GeorgiaTech\GeorgiaTech_IndustrialSystemsEngineering.csv'
df.to_csv(output_csv_file, index=False)

print("Scraping and CSV update complete.")
