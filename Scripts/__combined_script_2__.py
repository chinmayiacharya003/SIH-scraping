# from data import my_data 
from bs4 import BeautifulSoup
import os 
import time
import requests
import pandas as pd
from datetime import date

##! ----------- C O N S T A N T S -----------
RED = "\033[91m"  ## ? ERRORS / UNSUCCESSFUL OPERATION
GREEN = "\033[92m"  ## ? SUCCESSFUL OPERATION
YELLOW = "\033[93m"  ## ? WARNING
BLUE = "\033[94m"
RESET = "\033[0m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
}
REQUEST_DELAY = 2
REFERENCE_HTML = "reference.html"
HREF_TXT = "hrefs.txt"
TODAY_DATE = str(date.today())
MAX_TITLE_LENGTH = 20

##! ----------- F U N C T I O N S -----------
def make_request(request_url, set_headers):
    time.sleep(REQUEST_DELAY)
    print(f"Request URL: {request_url}")

    headers = HEADERS if set_headers == 'true' else None
    response = requests.get(url=request_url, headers=headers)

    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"{RED}Request to {request_url} failed with status code {response.status_code}{RESET}")
        return None

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"{GREEN}Directory '{directory_path}' created successfully {RESET}")
    else:
        print(f"{YELLOW}Directory '{directory_path}' already exists{RESET}")

def clean_title(title):
    cleaned_title = ''.join(e for e in title if e.isalnum() or e.isspace())
    cleaned_title = cleaned_title[:MAX_TITLE_LENGTH]
    return cleaned_title

def create_reference_html(dir_name, container):
    create_directory(dir_name)
    PATH_FOR_REF_HTML = os.path.join(dir_name, REFERENCE_HTML)
    
    with open(PATH_FOR_REF_HTML, "wb") as file:
        file.write(container.prettify().encode("utf-8"))
    
    print(f"{BLUE}\n-----------------------------------------------------{RESET}")
    print(f"{GREEN}Successfully created reference.html file for {dir_name}{RESET}")

def write_hrefs_to_file(dir_name, href_list):
    PATH_FOR_HREF_TXT = os.path.join(dir_name, HREF_TXT)
    cleaned_href_list = filter(None, href_list)
    
    with open(PATH_FOR_HREF_TXT, "w") as file:
        file.writelines("\n\n".join(cleaned_href_list))

    print(f"{GREEN}Successfully created hrefs.txt file for {dir_name}{RESET}")
    print(f"{BLUE}-----------------------------------------------------\n{RESET}")

def make_article_file(title, paragraphs, name):
    cleaned_title = clean_title(title)
    directory_path = os.path.join(name, TODAY_DATE)
    create_directory(directory_path=directory_path)
    PATH_TO_ARTICLE_TXT = os.path.join(name, TODAY_DATE, f"{cleaned_title}.txt")

    with open(PATH_TO_ARTICLE_TXT, "w", encoding="utf-8") as article:
        article.write(paragraphs)

    print(f"{GREEN}Article '{cleaned_title}' created successfully{RESET}\n")

##! ----------- M A I N   S C R A P I N G   L O G I C -----------
def scrape_content(name, main_url, wrp, ctn, sub_wrp, sub_ctn, set_headers):
    soup = make_request(request_url=main_url, set_headers=set_headers)

    if soup:
        main_article_ctn = soup.find(f"{wrp}", {"class": ctn})

        if main_article_ctn:
            create_reference_html(name, main_article_ctn)

            anchor_elements = main_article_ctn.find_all("a")
            href_list = [a.get("href") for a in anchor_elements]
            write_hrefs_to_file(name, href_list)

            for url in filter(None, href_list):
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = main_url + url

                ##! print(url)

                soup_2 = make_request(request_url=url, set_headers=set_headers)

                if soup_2 is not None:
                    title_element = soup_2.find("title")

                    if title_element:
                        title = title_element.text
                    else:
                        print(f"{RED}Title not found on the webpage{RESET}\n")
                        continue

                    ##! print(f"{sub_wrp} is the wrapper and {sub_ctn} is the sub container")

                    article_content = soup_2.find(f"{sub_wrp}", {"class": f"{sub_ctn}"})

                    if article_content:
                        paragraphs = article_content.text
                        make_article_file(title, paragraphs, name)
                    else:
                        print(f"{RED}Article Content is Empty{RESET}\n")

                else:
                    print(f"{RED}Failed to retrieve the webpage{RESET}\n")

        else:
            print(f"{RED}Unable to create reference.html file for {name}, class {ctn}{RESET}\n")

##! ----------- M A I N   F U N C T I O N -----------
def main():
    df = pd.read_excel('my_data.xlsx')

    for index, row in df.iterrows():
        name = row['name']
        url = row['url']
        wrapper = row['wrapper']
        ctn = row['container']
        subWrapper = row['subWrapper']
        subCtn = row['subContainer']
        set_headers = str(row['headers']).lower()

        scrape_content(name, url, wrapper, ctn, subWrapper, subCtn, set_headers)

if __name__ == "__main__":
    os.system('clear')
    main()

