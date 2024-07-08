import requests
from bs4 import BeautifulSoup
import csv
import os

# URL of the webpage to scrape
url = "https://be.mit.edu/directory"

# Define headers to make requests look like they come from a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def fetch_page_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None


def extract_email(profile_url):
    try:
        # Fetch the profile page content
        response = requests.get(profile_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the email link tag in the specified structure
        email_tag = soup.find('a', href=lambda x: x and x.startswith('mailto:'))

        # Get the email address from the href attribute or text of the <a> tag
        if email_tag:
            email = email_tag.get_text()
            return email
        else:
            return None

    except requests.RequestException as e:
        print(f"Error fetching the profile URL: {e}")
        return None


def extract_faculty_info(directory_url):
    content = fetch_page_content(directory_url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    faculty_list = []

    faculty_members = soup.find_all('tr', class_=['even', 'odd'])

    for member in faculty_members:
        faculty_info = {
            'University': 'MIT',
            'Department': 'Biological Engineering',
            'Name': 'N/A',
            'Position': 'N/A',
            'Link': 'N/A',
            'Email': 'N/A',
            'Research Focus': 'N/A',
        }

        name_tag = member.select_one(
            '.views-field-field-faculty-name-first-last- a')
        if name_tag:
            first_name = name_tag.text.strip()
            last_name_tag = member.select_one(
                '.views-field-field-faculty-last-name-for-alph a')
            last_name = last_name_tag.text.strip() if last_name_tag else 'N/A'
            full_name = f"{first_name} {last_name}".strip()
            faculty_info['Name'] = full_name

            profile_link = name_tag.get('href').strip()
            full_profile_link = f"https://be.mit.edu{profile_link}"
            faculty_info['Link'] = full_profile_link
            faculty_info['Email'] = extract_email(full_profile_link)

        position_tag = member.select_one('.views-field-field-faculty-rank')
        if position_tag:
            faculty_info['Position'] = position_tag.text.strip()

        research_focus_tag = member.select_one(
            '.views-field-field-faculty-research-areas')
        if research_focus_tag:
            faculty_info['Research Focus'] = research_focus_tag.text.strip()

        faculty_list.append(faculty_info)

    return faculty_list


def save_to_csv(faculty_info_list, csv_file_path):
    fieldnames = ['University', 'Department', 'Name', 'Position', 'Link',
                  'Email', 'Research Focus']
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for faculty_info in faculty_info_list:
            writer.writerow(faculty_info)
    print(f"Data saved to {csv_file_path}")


if __name__ == "__main__":
    faculty_info_list = extract_faculty_info(url)
    if faculty_info_list:
        csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_Biological_Engineering.csv"
        save_to_csv(faculty_info_list, csv_file_path)
