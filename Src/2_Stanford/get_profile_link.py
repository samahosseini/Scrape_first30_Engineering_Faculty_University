import pandas as pd
import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        print(f"Detected encoding: {result['encoding']}")
        return result['encoding']


def read_csv_file(input_csv):
    encoding = detect_encoding(input_csv)
    try:
        df = pd.read_csv(input_csv, encoding=encoding)
        print(f"File read successfully with encoding: {encoding}")
        return df
    except Exception as e:
        print(f"Failed to read the file with detected encoding: {encoding}")
        raise e


def extract_profile_link_and_email(driver, page_url):
    try:
        driver.get(page_url)
        time.sleep(3)  # wait for the page to load

        # Extract HTML content and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the profile link div
        div = soup.find('div',
                        class_='node stanford-person su-person-profile-link link label-hidden')
        profile_link = None
        if div:
            link = div.find('a', href=True)
            if link:
                profile_link = link['href']

        # Find the email in the required div
        email_div = soup.find('div', class_='su-person-email')
        email_tag = email_div.find('a', href=True) if email_div else None
        email = None
        if email_tag:
            email = email_tag['href'].replace('mailto:', '')

        return profile_link, email

    except Exception as e:
        print(f"An error occurred for URL: {page_url}", e)
        return None, None


def process_csv(input_csv, output_csv, error_log_csv):
    df = read_csv_file(input_csv)
    df.columns = df.columns.str.strip()
    print("Columns found in CSV:", df.columns)

    if 'Link' not in df.columns:
        print("The CSV file must contain a 'Link' column.")
        return

    df = df.iloc[194:] # Process only the first 10 rows

    profile_links = []
    emails = []
    errors = []

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()  # make sure ChromeDriver is in your PATH

    for index, row in df.iterrows():
        page_url = row['Link']
        profile_link, email = extract_profile_link_and_email(driver, page_url)
        profile_links.append(profile_link)
        emails.append(email)

        if profile_link is None and email is None:
            errors.append(page_url)

    # Close the WebDriver
    driver.quit()

    df['Profile_link'] = profile_links
    df['Email'] = emails
    df.to_csv(output_csv, index=False)

    # Log errors if there are any
    if errors:
        error_df = pd.DataFrame(errors, columns=['URL'])
        error_df.to_csv(error_log_csv, index=False)
        print(f"Error log saved to {error_log_csv}")

    print(f"Updated CSV saved to {output_csv}")


def main():
    input_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\2_Stanford\Primary_info.csv"
    output_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\2_Stanford\Secondary_info2.csv"
    error_log_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\2_Stanford\error_log.csv"
    process_csv(input_csv, output_csv, error_log_csv)


if __name__ == "__main__":
    main()
