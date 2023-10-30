import requests
from bs4 import BeautifulSoup
import time
from datetime import date
import os

## ! CONSTANTS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
}
MAIN_URL = "https://aninews.in/"
CONTAINER = {"itemprop": "articleBody"}

## ! COLORS
RED = "\033[91m"  ## ? ERRORS / UNSUCCESSFUL OPERATION
GREEN = "\033[92m"  ## ? SUCCESSFUL OPERATION
YELLOW = "\033[93m"  ## ? WARNING
BLUE = "\033[94m"
RESET = "\033[0m"

## ! FILE / DIR NAMES
DIR = "ANI"
TODAY_DIR = str(date.today())


PATH_TODAY_DIR = os.path.join(DIR, TODAY_DIR)

try:
    os.makedirs(PATH_TODAY_DIR)
    print(GREEN + "Directory created successfully" + RESET)
except OSError as e:
    print(YELLOW + f"Failed to create directory: {e}" + RESET)


## ! FUNCTIONS
# def check_article_length(PATH_TO_ARTICLE_TXT):
#     return os.path.getsize(PATH_TO_ARTICLE_TXT) == 0


def make_article_file(title, paragraphs):
    cleaned_title = title.replace('"', "")
    cleaned_title = cleaned_title.replace(" ", "_")
    cleaned_title = cleaned_title.replace(":", "")
    PATH_TO_ARTICLE_TXT = os.path.join(PATH_TODAY_DIR, cleaned_title)

    for paragraph in paragraphs:
        with open(f"{PATH_TO_ARTICLE_TXT}.txt", "a") as article:
            article.write(str(paragraph))

    print(
        GREEN
        + f" ARTICLE NAMED {BLUE}{cleaned_title}{RESET} {GREEN} created successfully "
        + RESET
    )

    # if check_article_length(PATH_TO_ARTICLE_TXT):
    #     print(GREEN + "Content written successfully" + RESET)
    # else:
    #     print(RED + "But Article content is Empty!" + RESET)


def main():
    with open(f"{DIR}/hrefs.txt", "r") as file:
        for url in file:
            url = url.strip()  ## ? Removes all Whitespaces

            if not url:
                continue

            if not url.startswith("http://") and not url.startswith("https://"):
                url = MAIN_URL + url

            response = requests.get(url, headers=HEADERS)
            time.sleep(3)  ## ! Delay of 3 seconds, necessary to prevent IP ban

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title_element = soup.find("title")

                if title_element:
                    title = title_element.text
                else:
                    print(RED + "Title not found on the webpage:", url + RESET)

                article_content = soup.find(
                    "div", {"itemprop": f"{CONTAINER['itemprop']}"}
                )

                if article_content:
                    paragraphs = article_content.find_all("p")
                else:
                    print(RED + "Article Content is Empty" + RESET)

                make_article_file(title, paragraphs)

            else:
                print(RED + f"Failed to retrieve the webpage: {url}" + RESET)


if __name__ == "__main__":
    main()
