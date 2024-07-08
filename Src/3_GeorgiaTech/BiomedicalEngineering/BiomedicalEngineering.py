import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the faculty page
url = 'https://bme.gatech.edu/bme/faculty'

# Send a request to fetch the HTML content of the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to hold the data
    data = []

    # Extract specific data - names, positions, emails, and research focuses
    faculty_list = soup.find_all('div', class_='views-row')

    for faculty in faculty_list:
        name_div = faculty.find('div', class_='views-field-field-last-name')
        name = name_div.find('a').get_text(strip=True) if name_div else 'N/A'
        link = name_div.find('a')['href'] if name_div else 'N/A'
        link = f"https://bme.gatech.edu{link}" if link != 'N/A' else 'N/A'

        position_div = faculty.find('div', class_='views-field-field-title')
        position = position_div.get_text(strip=True) if position_div else 'N/A'

        email_div = faculty.find('div', class_='views-field views-field-mail')
        email_anchor = email_div.find('a') if email_div else None
        email = email_anchor['href'].replace('mailto:',
                                             '') if email_anchor else 'N/A'

        research_div = faculty.find('div',
                                    class_='views-field-field-research-summary')
        research_focus = research_div.get_text(
            strip=True) if research_div else 'N/A'

        # Add the data to the list
        data.append({
            'University': 'GeorgiaTech',
            'Department': 'BiomedicalEngineering',
            'Name': name,
            'Position': position,
            'Link': link,
            'Email': email,
            'Research Focus': research_focus
        })

    # Convert the list to a DataFrame
    df = pd.DataFrame(data)

    # Define the output path
    output_path = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\3_GeorgiaTech\GeorgiaTech_BiomedicalEngineering.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False)

    print(f"Data successfully saved to {output_path}")
else:
    print(
        f"Failed to retrieve the webpage. Status code: {response.status_code}")
