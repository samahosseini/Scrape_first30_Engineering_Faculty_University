import requests
from bs4 import BeautifulSoup
import csv


def get_profile_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    profile_links = []

    # Find all links to individual profile pages
    for profile_div in soup.find_all('div', class_='views-field-title'):
        a_tag = profile_div.find('a', href=True)
        if a_tag:
            profile_links.append(f"https://www.mse.gatech.edu{a_tag['href']}")

    return profile_links


def extract_researcher_info(profile_url):
    profile = {
        'University': 'GeorgiaTech',
        'Department': 'Engineering',
        'Name': 'N/A',
        'Position': 'N/A',
        'Link': profile_url,
        'Email': 'N/A',
        'Research Focus': 'N/A'
    }

    return profile


def scrape_all_profiles(base_url):
    profile_links = get_profile_links(base_url)
    profiles = []

    for profile_link in profile_links:
        profiles.append(extract_researcher_info(profile_link))

    return profiles


def save_profiles_to_csv(profiles, filename):
    # Define the CSV column headers
    headers = profiles[0].keys()

    # Open the CSV file for writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header row
        writer.writeheader()

        # Write the profile rows
        writer.writerows(profiles)


# Main page URL with the list of researchers
base_url = 'https://www.mse.gatech.edu/people'

# Scrape all profiles
profiles = scrape_all_profiles(base_url)

# Save the profiles to a CSV file
csv_filename = 'x.csv'
save_profiles_to_csv(profiles, csv_filename)

print(f"Profiles saved to {csv_filename}")
