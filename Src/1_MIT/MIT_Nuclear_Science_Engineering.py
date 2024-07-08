import requests
from bs4 import BeautifulSoup
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import NoSuchElementException

# URL of the page containing faculty members
faculty_page_url = "http://web.mit.edu/nse/people/faculty/"

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


def scrape_faculty_info(url):
    # Path to your msedgedriver.exe
    driver_path = r'D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Data\msedgedriver.exe'

    # Set up the service for Edge Browser
    service = EdgeService(executable_path=driver_path)
    driver = webdriver.Edge(service=service)

    try:
        # Open the webpage
        driver.get(url)

        # Extract the name
        try:
            name_element = driver.find_element(By.TAG_NAME, 'h1')
            name = name_element.text.strip() if name_element else 'N/A'
        except NoSuchElementException:
            name = 'N/A'

        # Extract the position
        try:
            position_element = driver.find_element(By.XPATH,
                                                   '//h1/following-sibling::p')
            position = position_element.text.strip() if position_element else 'N/A'
        except NoSuchElementException:
            position = 'N/A'

        # Extract the email
        try:
            email_element = driver.find_element(By.XPATH,
                                                '//a[@class="mailto"]')
            email = email_element.get_attribute('href').replace('mailto:',
                                                                '') \
                if email_element else 'N/A'
        except NoSuchElementException:
            email = 'N/A'

        # Extract the research focus
        try:
            email_element = driver.find_element(By.XPATH,
                                                '//a[@class="mailto"]')
            email = email_element.get_attribute('href').replace('mailto:',
                                                                '') if email_element else 'N/A'

            # Extract the research focus
            text_div_element = driver.find_element(By.CLASS_NAME, 'text')
            research_focus_elements = text_div_element.find_elements(
                By.TAG_NAME, 'p')
            last_p_tag = research_focus_elements[-1]  # Get the last <p> tag

            research_focus_list = [a.text for a in
                                   last_p_tag.find_elements(By.CLASS_NAME,
                                                            'external')]
            research_focus = "\n    ".join(research_focus_list)
        except NoSuchElementException:
            research_focus = 'N/A'

        # Prepare the result as a dictionary
        result = {
            "University": 'MIT',
            "Department": 'Nuclear Science and Engineering',
            "Name": name,
            "Position": position,
            "Link": url,
            "Email": email,
            "Research Focus": research_focus
        }

        return result

    finally:
        # Close the WebDriver
        driver.quit()


def extract_faculty_urls(page_url):
    content = fetch_page_content(page_url)
    if not content:
        return []

    soup = BeautifulSoup(content, 'html.parser')
    relative_urls = soup.find_all('a', href=True)

    faculty_urls = []

    for tag in relative_urls:
        href = tag['href']
        if href.startswith('/nse/people/faculty'):
            full_url = "http://web.mit.edu" + href
            faculty_urls.append(full_url)

    return faculty_urls


def save_to_csv(faculty_info_list, csv_file_path):
    fieldnames = ["University", "Department", "Name", "Position", "Link",
                  "Email", "Research Focus"]
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for faculty_info in faculty_info_list:
            writer.writerow(faculty_info)
    print(f"Data saved to {csv_file_path}")


if __name__ == "__main__":
    # Extract faculty URLs
    faculty_urls = extract_faculty_urls(faculty_page_url)
    faculty_info_list = []

    # Loop through each faculty URL to scrape the information
    for url in faculty_urls:
        faculty_info = scrape_faculty_info(url)
        if faculty_info:
            faculty_info_list.append(faculty_info)

    # Define the CSV file path
    csv_file_path = "D:\\Files\\Upwork\\Scrape\\Us_30_Uni_engineering\\Result\\1_MIT\\MIT_1_NuclearScienceEngineering.csv"

    # Save the scraped data to CSV
    save_to_csv(faculty_info_list, csv_file_path)
