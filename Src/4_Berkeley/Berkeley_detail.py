import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_data(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract position
    position_tag = soup.find('p', class_='large')
    position = position_tag.get_text(strip=True) if position_tag else ""

    # Extract email
    email_tag = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
    email = email_tag.get_text(strip=True) if email_tag else ""

    # Extract research expertise
    expertise_heading = soup.find('h2', text='Research Expertise and Interest')
    expertise_tag = expertise_heading.find_next_sibling(
        'p') if expertise_heading else None
    research_expertise = expertise_tag.get_text(
        strip=True) if expertise_tag else ""

    # Clean up extra spaces in research expertise
    research_expertise = ' '.join(research_expertise.split())

    return {
        "Position": position,
        "Email": email,
        "Research Focus": research_expertise,
    }


# Path to the CSV file
csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\filtered_profiles_urls.csv'

# Read the CSV file
df = pd.read_csv(csv_file)

# Initialize new columns in the DataFrame
df['Position'] = ''
df['Email'] = ''
df['Research Focus'] = ''

# Loop through URLs and scrape data
for index, row in df.iterrows():
    url = row['Link']  # Assuming the column containing URLs is named 'Link'
    scraped_data = scrape_data(url)
    df.at[index, 'Position'] = scraped_data["Position"]
    df.at[index, 'Email'] = scraped_data["Email"]
    df.at[index, 'Research Focus'] = scraped_data["Research Focus"]

# Save the updated DataFrame back to the CSV
output_csv_file = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\4_Berkeley\Berkeley_Engineering.csv'
df.to_csv(output_csv_file, index=False)

print("Scraping and CSV update complete.")
