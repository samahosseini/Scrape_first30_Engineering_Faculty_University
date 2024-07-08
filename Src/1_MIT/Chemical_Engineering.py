import requests
from bs4 import BeautifulSoup
import time
import re
import csv

# URL of the page containing faculty members
url = "https://cheme.mit.edu/people/faculty/"

# Define headers to make requests look like they come from a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def fetch_page_content(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.content
        except (requests.RequestException, requests.Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All attempts failed.")
                return None

def extract_email(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        email_tag = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
        if email_tag:
            email = email_tag.get('href').replace('mailto:', '').strip()
            return email
        else:
            email_span = soup.find('span', class_='info-block-value')
            if email_span and 'mailto:' in email_span.parent.get('href', ''):
                email = email_span.get_text(strip=True)
                return email

            text = soup.get_text()
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
            if email_match:
                return email_match.group(0)

        return "N/A"
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return "N/A"

def extract_faculty_info(url):
    content = fetch_page_content(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    faculty_list = []

    faculty_divs = soup.find_all('div', class_='cheme-faculty-text')
    for div in faculty_divs:
        faculty_info = {
            'University': 'MIT',
            'Department': 'Chemical Engineering',
            'Name': 'N/A',
            'Position': 'N/A',
            'Link': 'N/A',
            'Email': 'N/A',
            'Research Focus': 'N/A',
        }

        name_tag = div.find('h2', class_='faculty-name').find('a')
        if name_tag:
            faculty_info['Name'] = name_tag.text.strip()
            profile_link = name_tag.get('href').strip()
            faculty_info['Link'] = profile_link
            faculty_info['Email'] = extract_email(profile_link)

        position_tag = div.find('div', class_='faculty-title')
        if position_tag:
            faculty_info['Position'] = position_tag.text.strip().replace('<br>', ' ')

        try:
            profile_content = fetch_page_content(profile_link)
            if profile_content:
                profile_soup = BeautifulSoup(profile_content, 'html.parser')
                research_interests_section = profile_soup.find(class_=
                                                               'cheme-profile-content')
                if research_interests_section:
                    research_interests_heading = (research_interests_section.
                                                  find('h2', text='Research Interests'))
                    if research_interests_heading:
                        research_focus = (research_interests_heading.
                                          find_next_sibling('p').text.strip())
                        faculty_info['Research Focus'] = research_focus
        except Exception as e:
            faculty_info['Research Focus'] = 'N/A'

        faculty_list.append(faculty_info)

    return faculty_list

def save_to_csv(faculty_info_list, csv_file_path):
    fieldnames = ['University', 'Department', 'Name', 'Position', 'Link', 'Email', 'Research Focus']
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for faculty_info in faculty_info_list:
            writer.writerow(faculty_info)
    print(f"Data saved to {csv_file_path}")

if __name__ == "__main__":
    faculty_info_list = extract_faculty_info(url)
    if faculty_info_list:
        csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_ChemicalEngineering.csv"
        save_to_csv(faculty_info_list, csv_file_path)