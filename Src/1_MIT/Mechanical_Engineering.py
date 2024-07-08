import requests
from bs4 import BeautifulSoup
import time
import re
import csv

# URL of the page containing faculty members
url = "https://meche.mit.edu/people"

# Define headers to make requests look like they come from a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
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

def extract_email_and_research(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract email
        email_tag = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
        email = email_tag.get('href').replace('mailto:', '').strip() if email_tag else "N/A"

        # Extract research focus
        research_focus = ""
        research_focus_tag = soup.find('div', {'class': 'interests'})
        if research_focus_tag:
            research_focus_ol = research_focus_tag.find('ol', {'class': 'numeric'})
            if research_focus_ol:
                research_focus_items = research_focus_ol.find_all('li', {'class': 'inverted'})
                research_focus = "\n    ".join([item.text.strip() for item in research_focus_items])

        return email, research_focus

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return "N/A", ""

def extract_faculty_info(url):
    content = fetch_page_content(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    faculty_list = []

    # Find all 'a' tags with the class 'clearfix' to get links to faculty profiles
    faculty_links = soup.find_all('a', class_='clearfix')
    for link in faculty_links:
        faculty_info = {
            'University': 'MIT',
            'Department': 'Mechanical Engineering',
            'Name': 'N/A',
            'Position': 'N/A',
            'Link': 'N/A',
            'Email': 'N/A',
            'Research Focus': '',
        }

        relative_url = link['href']
        full_url = f"https://meche.mit.edu{relative_url}"

        # Extract the Name and Position from the faculty link
        name_tag = link.find('span', class_='name')
        position_tag = link.find('span', class_='title')
        if name_tag and position_tag:
            faculty_info['Name'] = name_tag.text.strip()
            faculty_info['Position'] = position_tag.text.strip()
            faculty_info['Link'] = full_url
            faculty_info['Email'], faculty_info['Research Focus'] = extract_email_and_research(full_url)

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
        # Update the CSV file path as needed
        csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_MechanicalEngineering.csv.csv"
        save_to_csv(faculty_info_list, csv_file_path)
