import requests
from bs4 import BeautifulSoup

def scrape_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming the article content is in <p> elements, adjust the selector accordingly
        paragraphs = soup.find_all('p')

        # Combine text from all paragraphs
        article_content = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)

        # Return the article content
        return article_content
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

# Read URLs from the file
with open('file_1.txt', 'r') as file:
    urls = [line.strip() for line in file]

# Add 'https://assam.news18.com/' to each URL
base_url = 'https://assam.news18.com/'
urls = [base_url + url if not url.startswith('http') else url for url in urls]

# Scrape and save article content for each URL
for i, url in enumerate(urls, start=1):
    article_content = scrape_article_content(url)
    if article_content:
        with open(f'Assamese_File_{i}.txt', 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f"Article content saved to Assamese_File_{i}.txt for URL: {url}")
    else:
        print(f"Failed to retrieve article content for URL: {url}")
