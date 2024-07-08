import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_departments(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch the URL: {url}")
        return {'email': None, 'research_focus': None}

    soup = BeautifulSoup(response.content, 'html.parser')

    email_div = soup.find("div", class_="field--name-field-person-email")
    email = email_div.find("a").get_text() if email_div else None

    research_div = soup.find("div", class_="field--name-field-person-research")
    research_focus = None
    if research_div:
        ul_element = research_div.find("ul")
        if ul_element:
            research_list = ul_element.find_all("li")
            research_focus = [item.get_text(strip=True) for item in research_list]

    return {
        'email': email,
        'research_focus': research_focus
    }

# Prepare CSV paths
input_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Src\3_GeorgiaTech\faculty_info.csv"
output_csv = r"D:\Files\Upwork\Scrape\Us_30_Uni_engineering\Result\3_GeorgiaTech\GeorgiaTech_Aerospace_Engineering.csv"

# Read input CSV
df = pd.read_csv(input_csv)

# Ensure 'Link' column exists
if 'Link' not in df.columns:
    raise Exception("The CSV file must contain a 'Link' column")

# Initialize output columns
df['Email'] = ""
df['Research Focus'] = ""
df['University'] = "GeorgiaTech"
df['Department'] = "Aerospace Engineering"

# Process each URL in the 'Link' column
for index, row in df.iterrows():
    url = row['Link']
    result = extract_departments(url)
    print(result['email'], result['research_focus'])
    df.at[index, 'Email'] = result['email']
    df.at[index, 'Research Focus'] = ", ".join(result['research_focus']) if result['research_focus'] else None

# Rearrange columns in the desired order
df = df[['University', 'Department', 'Name', 'Position', 'Link', 'Email', 'Research Focus']]

# Save the updated dataframe to the output CSV
df.to_csv(output_csv, index=False)
print(f"Updated CSV saved to {output_csv}")
