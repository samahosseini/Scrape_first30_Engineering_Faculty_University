import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_departments(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    department_tags = soup.find_all('span', class_='department')

    departments = []
    for tag in department_tags:
        text = tag.get_text()
        if 'Department:' in text:
            department = text.split('Department:')[1]
            department = department.replace('\xa0', ' ').replace('&nbsp;', ' ').strip()
            department = ' '.join(department.split())
            departments.append(department)

    return ", ".join(departments) if departments else None


def extract_research_focus(url):
    response = requests.get(url)

    if response.status_code != 200:
        return 'N/A'

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with the specific id
    research_section = soup.find('div', id='currentResearchAndScholarlyInterestsContent')

    # Extract the text within the <p> tag
    if research_section:
        research_text = research_section.find('p').get_text()
        return research_text
    else:
        return 'N/A'


def read_csv_file(input_csv):
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    last_exception = None
    for encoding in encodings:
        try:
            # Attempt to read the CSV file using different encodings
            print(f"Trying to read the file {input_csv} with encoding {encoding}")
            df = pd.read_csv(input_csv, encoding=encoding, delimiter=',|\t', engine='python', skip_blank_lines=True, on_bad_lines='warn')
            print(f"File read successfully with encoding: {encoding}")
            return df
        except (UnicodeDecodeError, pd.errors.ParserError) as e:
            print(f"Failed to read the file with encoding: {encoding}")
            last_exception = e
    # Print the last encountered exception for more debugging information
    print(f"Last encountered exception: {last_exception}")
    raise ValueError(f"Unable to decode the file {input_csv} using any common encodings. Please verify the CSV file encoding.")


def process_csv(input_csv, output_csv):
    df = read_csv_file(input_csv)

    # Trim any leading/trailing whitespace characters from the column names
    df.columns = df.columns.str.strip()

    # Print columns to ensure correct reading
    print("Columns found in CSV:", df.columns)

    if 'Profile_link' not in df.columns:
        print("The CSV file must contain a 'Profile_link' column.")
        return

    df['Department'] = df['Profile_link'].apply(extract_departments)
    df['Research Focus'] = df['Profile_link'].apply(extract_research_focus)
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")


def main():
    input_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\2_Stanford\Secondary_info.csv"
    output_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\2_Stanford\Stanford_final_faculty_info.csv"
    process_csv(input_csv, output_csv)


if __name__ == "__main__":
    main()
