import requests
import os
from bs4 import BeautifulSoup

## ! CONSTANTS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
}
URL = "https://timesofindia.indiatimes.com/"
CONTAINER = {
    "class": "BUoQz"
}  ## ? Container is a 'id' attribute
HEADERS = False ## ? Headers = False when Headers are not to be included

## ! COLORS
RED = "\033[91m"  ## ? ERRORS / UNSUCCESSFUL OPERATION
GREEN = "\033[92m"  ## ? SUCCESSFUL OPERATION
YELLOW = "\033[93m"  ## ? WARNING
BLUE = "\033[94m"
RESET = "\033[0m"


## ! FILE / DIR NAMES
DIR_NAME = 'TOI'
DIR = os.path.join('Scripts', 'references', f"{DIR_NAME}")
REFERENCE_HTML = "reference.html"
HREF_TXT = "hrefs.txt"


## ! PATHS
try:
    os.makedirs(DIR)
    print(GREEN + "Directory created successfully" + RESET)
except OSError as e:
    print(YELLOW + f"Failed to create directory: {e}" + RESET)

PATH_FOR_REF_HTML = os.path.join(f"{DIR}", f"{REFERENCE_HTML}")
PATH_FOR_HREF_TXT = os.path.join(f"{DIR}", f"{HREF_TXT}")


## ! FUNCTIONS
def make_request():
    if HEADERS: 
        response = requests.get(url=URL, headers=HEADERS)
        return BeautifulSoup(response.text, "html.parser")
    else: 
        response = requests.get(url=URL)
        return BeautifulSoup(response.text, "html.parser")
    


def create_reference_html(container):
    with open(PATH_FOR_REF_HTML, "wb") as file:
        file.write(container.prettify().encode("utf-8"))


def find_write_href(anchor_list):
    # return [a.get("href") for a in anchor_list]
    with open(PATH_FOR_HREF_TXT, "w") as file:
        hrefElements = [a.get("href") for a in anchor_list]
        for href in hrefElements:
            file.write(href)
            file.write("\n\n")


def main():
    SOUP = make_request()

    if "class" in CONTAINER:
        articleContainer = SOUP.find("div", {"class": f"{CONTAINER['class']}"})
    else:
        articleContainer = SOUP.find("div", {"id": f"{CONTAINER['id']}"})

    if articleContainer:
        create_reference_html(articleContainer)
        anchorElements = articleContainer.find_all("a")
        find_write_href(anchorElements)

    else:
        print(RED + "Error in Creating reference.html file,\nCheck the Container" + RESET)


if __name__ == "__main__":
    main()
