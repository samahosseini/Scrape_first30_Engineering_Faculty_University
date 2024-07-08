import requests
from bs4 import BeautifulSoup
import time
import re
import csv
import os

# URL of the page containing faculty members
url = "https://cee.mit.edu/faculty/"

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


def extract_research_and_email(profile_url):
    response = fetch_page_content(profile_url)
    if not response:
        return "Error fetching the page", "Email information not found."

    soup = BeautifulSoup(response, 'html.parser')

    # Extracting Research Interests
    research_paragraphs = []
    research_heading = soup.find('h3', string="Research Interests")
    if research_heading:
        next_sibling = research_heading.find_next_sibling()
        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name in ['p', 'ul', 'li']:
                research_paragraphs.append(next_sibling.get_text(strip=True))
            next_sibling = next_sibling.find_next_sibling()
        research_paragraph = "\n".join(
            research_paragraphs) if research_paragraphs else "Research interests information not found."
    else:
        research_paragraph = "Research interests information not found."

    # Extracting Email
    email_tag = soup.find('a', href=lambda href: href and "mailto" in href)
    email = email_tag.text.strip() if email_tag else "Email information not found."

    return research_paragraph, email


def get_profile_urls(faculty_page_url):
    response = fetch_page_content(faculty_page_url)
    if not response:
        print("Error fetching the page.")
        return []

    soup = BeautifulSoup(response, 'html.parser')

    # Extract profile links based on the given classes
    classes = [
        'people-item climate-environment-life-science food-water-security faculty',
        'people-item sustainable-materials-infrastructure faculty',
        'people-item climate-environment-life-science faculty',
        'people-item resilient-systems-mobility faculty',
    ]

    profile_urls = []
    for class_name in classes:
        profile_links = soup.find_all('a', class_=class_name)
        profile_urls.extend(
            [link['href'] for link in profile_links if 'href' in link.attrs])

    return profile_urls


def extract_faculty_info(url):
    content = fetch_page_content(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    faculty_list = []

    # Extract Name and Position from the main faculty page
    profile_infos = []
    for profile in soup.select('.profile-content'):
        name = profile.find('h3').text.strip()
        position = profile.find('span').text.strip()
        profile_infos.append({
            'name': name,
            'position': position
        })

    # Get the profile URLs on the page
    profile_urls = get_profile_urls(url)

    # Process the profiles and append further information if URL matches
    for i in range(min(len(profile_infos), len(profile_urls))):
        full_url = requests.compat.urljoin(url, profile_urls[i])
        research_interests, email = extract_research_and_email(full_url)
        profile_infos[i].update({
            'url': full_url,
            'research_interests': research_interests,
            'email': email
        })

        # Add consolidated information to faculty list
        faculty_list.append({
            'University': 'MIT',
            'Department': 'Civil and Environmental Engineering',
            'Name': profile_infos[i]['name'],
            'Position': profile_infos[i]['position'],
            'Link': profile_infos[i]['url'],
            'Email': profile_infos[i]['email'],
            'Research Focus': profile_infos[i]['research_interests']
        })

    return faculty_list


def save_to_csv(faculty_info_list, csv_file_path):
    fieldnames = [
        'University', 'Department', 'Name', 'Position', 'Link',
        'Email', 'Research Focus'
    ]
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for faculty_info in faculty_info_list:
            writer.writerow(faculty_info)
    print(f"Data saved to {csv_file_path}")

if __name__ == "__main__":
    faculty_info_list = extract_faculty_info(url)
    if faculty_info_list:
        csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_CivilEngineering.csv"
        save_to_csv(faculty_info_list, csv_file_path)
    else:
        print("No faculty information found.")

