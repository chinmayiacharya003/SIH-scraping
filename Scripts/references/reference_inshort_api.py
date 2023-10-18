## --> Install 'Better Comments' vscode extension for better understanding <--

import requests
import json
import os

## --> Better Comments <--
##
# * This is an Information
# ! This is an Alert
# ? This is a Query
##

# ? Reference script to use inshorts news api to GET articles based on categories
# ! All .txt, .json files will be downloads into Assets\inshorts_downloads


def getNews(category):
    headers = {
        "authority": "inshorts.com",
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.5",
        "content-type": "application/json",
        "referer": "https://inshorts.com/en/read",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    params = (
        ("category", category),
        ("max_limit", "10"),
        ("include_card_data", "true"),
    )

    if category == "all":
        response = requests.get(
            f"https://inshorts.com/api/en/news?category=all_news&max_limit=10&include_card_data=true",
            headers=headers,
        )
    else:
        response = requests.get(
            f"https://inshorts.com/api/en/search/trending_topics/{category}",
            headers=headers,
            params=params,
        )

    try:
        news_data = response.json()["data"]["news_list"]
    except Exception as e:
        print(response.text)
        news_data = None

    return news_data


def create_download_dir(article_folder_path):
    if not os.path.exists(article_folder_path):
        ## * If the article does'nt exists, create one
        os.makedirs(article_folder_path)
        print(f"{article_folder_path} created successfully")
    else:
        print("Folder with this name already exists")


def write_json(json_file_path, source_of_json):
    with open(json_file_path, "w") as file:
        json.dump(source_of_json, file, indent=4)


def main():
    category = "national"

    ## * Following are some of the various categories
    # all
    # national //Indian News only
    # business
    # sports
    # world
    # politics
    # technology
    # startup
    # entertainment
    # miscellaneous
    # hatke
    # science
    # automobile

    news_data = getNews(category)

    ## * Article counter to create article{article_counter}.txt
    article_counter = 1
    article_folder_path = "Assets\inshorts_downloads\downloaded_article"

    ## * Logic to check if the dir "downloaded_articles" already exists or not
    create_download_dir(article_folder_path)

    ## * Iteration over the JSON file
    ## ! Refer the downloaded JSON file 'output.json' for better picture
    for each_news_article in news_data:
        try:
            author = each_news_article.get("news_obj", {}).get(
                "author_name", "No author"
            )
            content = each_news_article.get("news_obj", {}).get("content", "No content")
            source = each_news_article.get("news_obj", {}).get(
                "source_url", "No source"
            )

            article_contents = [author, content, source]

            ## * Logic to dynamically create the articles in 'downloaded_articles' dir
            article_name = f"article{article_counter}.txt"
            article_path = os.path.join(article_folder_path, article_name)

            with open(article_path, "a") as file:
                for content in article_contents:
                    file.write(content + "\n")

            article_counter += 1
        except Exception as e:
            print(f"Error processing an article: {e}")

    ## * Write the JSON file into 'output.json', refer it for better understanding of the 'GET' method results
    write_json("Assets\inshorts_downloads\output.json", news_data)


if __name__ == "__main__":
    main()


## ! For some reason the MIN and MAX number of article returned by the API is always 10
## ! The content in the article inside downloaded_articles yet to be cleaned
## ! Code yet to be optimized
## ! Optimization will be done upon finalization
