"""import requests
from bs4 import BeautifulSoup
import time
import csv

# URL of the page containing faculty members
main_url = "https://www.eecs.mit.edu/role/faculty/?fwp_role=faculty&fwp_research=robotics"

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


def extract_profile_urls(url):
    content = fetch_page_content(url)
    if not content:
        return []

    soup = BeautifulSoup(content, 'html.parser')
    profile_urls = []

    # Find all 'a' tags that are within 'h5' tags
    profile_links = soup.find_all('h5')
    for profile_link in profile_links:
        a_tag = profile_link.find('a', href=True)
        if a_tag:
            profile_urls.append(a_tag['href'])

    return profile_urls


def extract_faculty_info(url):
    content = fetch_page_content(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    faculty_info = {
        'University': 'MIT',
        'Department': 'Electrical Engineering and Computer Science',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': 'N/A',
        'Email': 'N/A',
        'Research Focus': 'N/A',
    }
    # Extract the name
    name_tag = soup.find('h1', class_='page-title')
    if name_tag:
        faculty_info['Name'] = name_tag.text.strip()

    # Extract the position and email
    position_div = soup.find('div',
                             class_='small-12 medium-5 large-4 bold-links cell')
    if position_div:
        position_p = position_div.find('p')
        if position_p:
            faculty_info['Position'] = position_p.text.strip()

        email_div = position_div.find('a', href=lambda x: x and x.startswith(
            'mailto:'))
        if email_div:
            faculty_info['Email'] = email_div.text.strip()

    # Extract the research focus
    research_focus = []
    research_areas = soup.find('div', class_='research-areas')
    if research_areas:
        research_items = research_areas.find_all('li')
        for item in research_items:
            research_focus.append(item.text.strip())

    if research_focus:
        faculty_info['Research_focus'] = "\n    ".join(research_focus)

    return faculty_info


def save_to_csv(faculty_info_list, csv_file_path):
    fieldnames = ['Name', 'Position', 'Email', 'Research_focus']
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for faculty_info in faculty_info_list:
            writer.writerow(faculty_info)
    print(f"Data saved to {csv_file_path}")


if __name__ == "__main__":
    profile_urls = extract_profile_urls(main_url)
    if profile_urls:
        faculty_info_list = []
        for profile_url in profile_urls:
            faculty_info = extract_faculty_info(profile_url)
            if faculty_info:
                faculty_info_list.append(faculty_info)

        # Update the CSV file path as needed
        csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_ElectricalEngineering_ComputerScience.csv"
        save_to_csv(faculty_info_list, csv_file_path)
"""
import requests
from bs4 import BeautifulSoup
import time
import csv


# URL of the main page containing faculty members
url = ("https://www.eecs.mit.edu/role/faculty/?fwp_role=faculty&fwp_"
       "research=robotics")

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


def extract_profile_urls(url):
    content = fetch_page_content(url)
    if not content:
        return []

    soup = BeautifulSoup(content, 'html.parser')
    profile_urls = []

    # Find all 'a' tags that are within 'h5' tags
    profile_links = soup.find_all('h5')
    for profile_link in profile_links:
        a_tag = profile_link.find('a', href=True)
        if a_tag:
            profile_urls.append(a_tag['href'])

    return profile_urls


def extract_faculty_info(url):
    content = fetch_page_content(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    faculty_info = {
        'University': 'MIT',
        'Department': 'Electrical Engineering and Computer Science',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': url,  # Include the profile URL
        'Email': 'N/A',
        'Research Focus': 'N/A'
    }

    # Extract the name
    name_tag = soup.find('h1', class_='page-title')
    if name_tag:
        faculty_info['Name'] = name_tag.text.strip()

    # Extract the position and email
    position_div = soup.find('div',
                             class_='small-12 medium-5 large-4 bold-links cell')
    if position_div:
        position_p = position_div.find('p')
        if position_p:
            faculty_info['Position'] = position_p.text.strip()

        email_div = position_div.find('a', href=lambda x: x and x.startswith(
            'mailto:'))
        if email_div:
            faculty_info['Email'] = email_div.text.strip()

    # Extract the research focus
    research_focus = []
    research_areas = soup.find('div', class_='research-areas')
    if research_areas:
        research_items = research_areas.find_all('li')
        for item in research_items:
            research_focus.append(item.text.strip())

    if research_focus:
        faculty_info['Research Focus'] = "\n    ".join(research_focus)

    return faculty_info


def save_to_csv(faculty_info_list, csv_file_path):
    fieldnames = ['University', 'Department', 'Name', 'Position', 'Link',
                  'Email', 'Research Focus']  # Update the field names
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for faculty_info in faculty_info_list:
            writer.writerow(faculty_info)
    print(f"Data saved to {csv_file_path}")


if __name__ == "__main__":
    profile_urls = extract_profile_urls(url)
    if profile_urls:
        faculty_info_list = []
        for profile_url in profile_urls:
            faculty_info = extract_faculty_info(profile_url)
            if faculty_info:
                faculty_info_list.append(faculty_info)

        csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_ElectricalEngineering_ComputerScience.csv"
        save_to_csv(faculty_info_list, csv_file_path)
