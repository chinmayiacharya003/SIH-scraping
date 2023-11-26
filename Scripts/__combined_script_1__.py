import requests
from bs4 import BeautifulSoup
from datetime import date
import os
import time


## ! --------------------------------------------------------------> COLORS
RED = "\033[91m"  ## ? ERRORS / UNSUCCESSFUL OPERATION
GREEN = "\033[92m"  ## ? SUCCESSFUL OPERATION
YELLOW = "\033[93m"  ## ? WARNING
BLUE = "\033[94m"
RESET = "\033[0m"

## ! --------------------------------------------------------------> CONSTANTS 
## ! MAIN CONSTANTS 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
}
MAIN_URL = "https://www.hindustantimes.com/"
SET_HEADERS = True ## ? Headers = False when Headers are not to be included
DELAY = 2 ## ? Delay in seconds b/w each request

## ! MAIN CONTAINER 
CONTAINER_TYPE = 'class'
CONTAINER_NAME = 'mainContainer'
CONTAINER = {
    CONTAINER_TYPE: CONTAINER_NAME
}

## ! SUB_CONTAINER
SUB_CONTAINER_TYPE = 'class'
SUB_CONTAINER_NAME = 'detail'
SUB_CONTAINER = {
    SUB_CONTAINER_TYPE: SUB_CONTAINER_NAME
}

## ! FILE / DIR NAMES
DIR_NAME = 'HT'
DIR = os.path.join('Scripts', 'references', f"{DIR_NAME}")
REFERENCE_HTML = "reference.html"
HREF_TXT = "hrefs.txt"

def create_main_dir():
    try:
        os.makedirs(DIR)
        print(GREEN + "Directory created successfully" + RESET)
    except OSError as e:
        print(YELLOW + f"Failed to create directory: {e}" + RESET)

TODAY_DIR = str(date.today())
PATH_TODAY_DIR = os.path.join(DIR, TODAY_DIR)

def create_today_dir():
    try:
        os.makedirs(PATH_TODAY_DIR)
        print(GREEN + "Directory created successfully" + RESET)
    except OSError as e:
        print(YELLOW + f"Failed to create directory: {e}" + RESET)

## ! PATHS
create_main_dir()
create_today_dir()  
PATH_FOR_REF_HTML = os.path.join(f"{DIR}", f"{REFERENCE_HTML}")
PATH_FOR_HREF_TXT = os.path.join(f"{DIR}", f"{HREF_TXT}")

## ! --------------------------------------------------------------> FUNCTIONS 
def make_request(REQUEST_URL):
    headers = HEADERS if SET_HEADERS else None
    time.sleep(DELAY)
    response = requests.get(url=REQUEST_URL, headers=headers)
    
    if response.status_code == 200: 
        return BeautifulSoup(response.text, "html.parser")
    else: 
        return None

def create_reference_html(container):
    with open(PATH_FOR_REF_HTML, "wb") as file:
        file.write(container.prettify().encode("utf-8"))
    print(GREEN + f"Successfully Created {BLUE} reference.html {GREEN} file" + RESET + '\n')

def find_write_href(anchor_list):
    with open(PATH_FOR_HREF_TXT, "w") as file:
        hrefElements = [a.get("href") for a in anchor_list]
        for href in hrefElements:
            if href is not None:
                file.write(href)
                file.write("\n\n")
    print(GREEN + f"Successfully Created {BLUE} hrefs.txt {GREEN} file" + RESET + '\n')

def shorten_title(title):
    words = title.split()
    if len(words) <= 10:
        return title
    else:
        return ' '.join(words[:10])

def make_article_file(title, paragraphs):
    cleaned_title = title.replace('"', "")
    cleaned_title = cleaned_title.replace(":", "")
    cleaned_title = cleaned_title.replace(",", "")
    cleaned_title = cleaned_title.replace("|", "")
    cleaned_title = cleaned_title.replace("-", "")
    cleaned_title = cleaned_title.replace("!", "")
    cleaned_title = cleaned_title.replace("?", "")
    cleaned_title = cleaned_title.replace("'", "")
    cleaned_title = "_".join(cleaned_title.split()) 

    shortened_title = shorten_title(cleaned_title)

    MAX_FILENAME_LENGTH = 255  ## ? Adjust accordingly 
    if len(shortened_title) > MAX_FILENAME_LENGTH:
        shortened_title = shortened_title[:MAX_FILENAME_LENGTH]

    PATH_TO_ARTICLE_TXT = os.path.join(PATH_TODAY_DIR, shortened_title)

    with open(f"{PATH_TO_ARTICLE_TXT}.txt", "w", encoding="utf-8") as article:
        article.write(paragraphs)

    print(
        GREEN
        + f" ARTICLE NAMED {BLUE}{cleaned_title}{RESET} {GREEN} created successfully "
        + RESET + '\n'
    )

## ! --------------------------------------------------------------> MAIN FUNCTIONS
def main():
    SOUP = make_request(MAIN_URL)

    ## ! 1) FETCH HREF PART 
    if "class" in CONTAINER:
        main_article_container = SOUP.find("section", {CONTAINER_TYPE: f"{CONTAINER['class']}"})
    else:
        main_article_container = SOUP.find("section", {CONTAINER_TYPE: f"{CONTAINER['id']}"})

    if main_article_container:
        create_reference_html(main_article_container)
        anchor_elements = main_article_container.find_all("a")
        find_write_href(anchor_elements)

        ## ! 2) FETCH CONTENT FROM HREF PART
        with open(f"{DIR}/hrefs.txt", "r") as file:
            for url in file:
                url = url.strip()  ## ? Removes all Whitespaces

                if not url:
                    continue

                if not url.startswith("http://") and not url.startswith("https://"):
                    url = MAIN_URL + url
            
                print(url)

                SOUP_2 = make_request(url)

                if SOUP_2 is not None: 
                    title_element = SOUP_2.find("title")

                    if title_element:
                        title = title_element.text
                    else:
                        print(RED + "Title not found on the webpage:", url + RESET + '\n')

                    article_content = SOUP_2.find(
                        "div", {f"{SUB_CONTAINER_TYPE}": f"{SUB_CONTAINER[SUB_CONTAINER_TYPE]}"}
                    )

                    paragraphs = ''

                    if article_content:
                        paragraphs = article_content.text
                        make_article_file(title, paragraphs)
                    else:
                        print(RED + "Article Content with title {title} is Empty" + RESET + '\n')
                
                else:
                    print(RED + f"Failed to retrieve the webpage: {url}" + RESET + '\n')

    else:
        print(RED + "Error in Creating reference.html file,\nCheck the Container" + RESET + '\n')

if __name__ == "__main__":
    os.system('clear') ## ? Clears the terminal screen
    main()
