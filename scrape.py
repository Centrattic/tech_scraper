from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import requests
import time
from tqdm import tqdm
from io import BytesIO

# Configuration
MIT_TECH_URL = 'https://thetech.com/issues'  # Replace with the correct URL if needed
KEYWORD1 = '120 bay state'# Replace with the keyword you want to search for
# KEYWORD1_2 = 'woman'  
# KEYWORD2 = 'east campus'

year1 = 60
year2 = 85
output_file = "output_bay_state.txt"

old_issue_links = [0]*60*(year2-year1)

for i in range(60): # 85 -99
    for j in range(year1, year2): # 60 
        old_issue_links[(j-year1)*(i)] = (f"https://thetech.com/issues/{j}/{i}/pdf")

try:

    for link in tqdm(old_issue_links):
        if link:
            try:
                # Download the PDF
                response = requests.get(link)
                soup = BeautifulSoup(response.content, 'html.parser')

                iframe = soup.find('iframe')
                if iframe:
                    src = iframe.get('src')

                    pdf_page = requests.get(src)
                    pdf_file = pdf_page.content

                    pdf_file = BytesIO(pdf_file)
                    text = extract_text(pdf_file)

                    # Search for the keyword
                    if KEYWORD1.lower() in text.lower():
                        with open(output_file, "a") as f:
                            f.write(f"Found keyword in {link}\n")

            except Exception as e:
                print(f"Error processing {link}: {e}")
                with open(output_file, "a") as f:
                    f.write(f"Error processing {link}: {e}\n")
except:
    print("Weird error")