from bs4 import BeautifulSoup
import PyPDF2
from pdfminer.high_level import extract_text
import requests
import time
from tqdm import tqdm
from io import BytesIO
import re

# Configuration
MIT_TECH_URL = 'https://thetech.com/issues'  # Replace with the correct URL if needed
KEYWORD1 = 'women' # Replace with the keyword you want to search for
KEYWORD1_2 = 'woman'  
KEYWORD2 = 'east campus'

women_links = []

with open("output.txt", "r") as f:
    for line in f:
        line_link = re.search(r'https?://\S+', line).group()
        women_links.append(line_link)
f.close()

issue_links_with_keyword = []

try:

    for link in tqdm(women_links):
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
                    if text.lower().count(KEYWORD1) >= 5 or text.lower().count(KEYWORD2) >= 5:
                        issue_links_with_keyword.append(link)
                        with open("output_wom.txt", "a") as f:
                            if KEYWORD2.lower() in text.lower():
                                f.write(f"Found WOMAN & EC keyword in {link}\n")
                            else:
                                f.write(f"Found WOMAN keyword in {link}\n")

            except Exception as e:
                print(f"Error processing {link}: {e}")
                with open("output.txt", "a") as f:
                    f.write(f"Error processing {link}: {e}\n")
except:
    print("Weird error")