# ---------------------------------------------------------------------------------------
#
# webscraper.py
#
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

from bs4 import BeautifulSoup as bs
# import pinkbike__database as pb_db
import requests

# ---------------------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------
# App initialization / configuration
# ---------------------------------------------------------------------------------------

# url = "https://www.pinkbike.com/news/archive/?catid=0&year=2020&month=1"
url = "https://www.pinkbike.com/news/pinkbike-poll-how-mechanically-minded-are-you.html"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers = headers)
html = response.text
soup = bs(html, "html.parser")


# Scrape this:
    # 1. article_title TEXT,
    # 2. article_url TEXT,
    # 3. article_author TEXT,
    # 4. article_number_of_comments INTEGER,
    # 5. article_description TEXT,
    # 6. article_publishing_date TEXT,
    # 7. TIMESTAMP DEFAULT CURRENT_TIMESTAMP

# article_title TEXT
def get_article_title(soup):
    article_titles = soup.find_all("a", { "class" : "f22 fgrey4 bold"})
    for article_title in article_titles:
        print(article_title.text.strip())

# article_url TEXT
def get_article_url(soup):
    article_urls = soup.find_all("a", { "class" : "f22 fgrey4 bold"}, href=True)
    for article_url in article_urls:
        print(article_url["href"])

# article_author TEXT
def get_article_author(soup):
    article_authors = soup.find_all("a", { "class" : "fblack"})
    for article_author in article_authors:
        print(article_author.text.strip())

# article_number_of_comments INTEGER
def get_article_number_of_comments(soup):
    article_numbers_of_comments = soup.find_all("div", { "class" : "floatleft"})
    for article_number_of_comments in article_numbers_of_comments:
        print(article_number_of_comments.contents[2].strip())

# article_description TEXT
def get_meta_description(soup):
    meta_description = soup.find("meta", {"name":"description"})["content"]
    print(meta_description)

# article_publishing_date TEXT
def get_published_time(soup):
    published_time = soup.find("meta", {"property":"article:published_time"})["content"]
    print(published_time)

# get_article_number_of_comments(soup)
# get_article_title(soup)
# get_article_url(soup)
# get_article_author(soup)
# get_meta_description(soup)
# get_published_time(soup)
