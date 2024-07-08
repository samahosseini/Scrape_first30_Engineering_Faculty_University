import requests
from bs4 import BeautifulSoup
import csv
import os

# URL of the webpage to scrape
url = "https://aeroastro.mit.edu/faculty/"

# Define headers to make requests look like they come from a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def extract_email(url):
    try:
        # Fetch the page content directly
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the email address
        email_tag = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
        email = email_tag.get_text() if email_tag else None
        return email

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def scrape_faculty_data():
    try:
        # Fetch the raw HTML content directly
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # List to store all professors' data
        faculty_data = []

        # Finding the faculty member sections
        faculty_members = soup.find_all('div', class_='tile')

        for member in faculty_members:
            try:
                faculty_info = {}
                faculty_info['University'] = 'MIT'
                faculty_info['Department'] = 'Aeronautics and Astronautics'

                # Extracting professor's name
                name_elem = member.find('div', class_='tile__title').find('h3')
                faculty_info['Name'] = name_elem.get_text(
                    strip=True) if name_elem else 'N/A'

                # Extracting professor's position
                position_elem = member.find('div',
                                            class_='tile__description').find(
                    'i')
                faculty_info['Position'] = position_elem.get_text(
                    strip=True) if position_elem else 'N/A'

                # Extracting the wrapping parent link
                parent_a = member.find_parent('a', href=True)
                if parent_a:
                    prof_url = parent_a['href']
                    faculty_info['Link'] = prof_url

                    # Fetch and extract the email from the professor's page
                    faculty_info['Email'] = extract_email(prof_url)
                else:
                    faculty_info['Link'] = 'N/A'
                    faculty_info['Email'] = 'N/A'

                # Extracting professor's research focus
                description_elem = member.find('div',
                                               class_='tile__description')
                if description_elem:
                    bold_elem = description_elem.find('b', text=lambda
                        t: t and t.startswith("Research Area"))
                    if bold_elem:
                        research_focus = bold_elem.next_sibling.strip() if bold_elem.next_sibling else bold_elem.next_element.strip()
                        faculty_info['Research Focus'] = research_focus
                    else:
                        faculty_info['Research Focus'] = 'N/A'
                else:
                    faculty_info['Research Focus'] = 'N/A'

                # Append the information to the list
                faculty_data.append(faculty_info)

            except Exception as e:
                print(f"Error processing a faculty member block: {e}")

        # Save the extracted data to a CSV file
        file_path = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\1_MIT\MIT_1_AeroAstro.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=faculty_data[0].keys())
            writer.writeheader()
            writer.writerows(faculty_data)

        print(f"Data saved to {file_path}")

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"Error parsing the HTML content: {e}")

if __name__ == "__main__":
    scrape_faculty_data()
