import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_faculty_info(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    faculty_data = []

    faculty_members = soup.find_all('div',
                                    class_='node node--type-dir-person node--view-mode-teaser')

    for member in faculty_members:
        # Extract name
        name_tag = member.select_one(
            "div.field--name-field-person-name .field__item")
        name = name_tag.get_text(strip=True) if name_tag else "Not Provided"

        # Extract position
        position_tag = member.select_one(
            "div.field--name-field-person-job-title-s- .field__item")
        position = position_tag.get_text(
            strip=True) if position_tag else "Not Provided"

        # Extract profile URL
        link_tag = member.select_one("a.dir_link")
        base_url = "https://ae.gatech.edu"
        profile_url = base_url + link_tag[
            'href'] if link_tag else "Not Available"

        faculty_data.append({
            "Name": name,
            "Position": position,
            "Link": profile_url
        })

    return faculty_data


def save_to_csv(data, output_csv):
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Academic faculty data saved to {output_csv}")


def main():
    url = "https://ae.gatech.edu/academic-faculty-1"
    output_csv = "faculty_info.csv"

    faculty_info = extract_faculty_info(url)
    save_to_csv(faculty_info, output_csv)


if __name__ == "__main__":
    main()
