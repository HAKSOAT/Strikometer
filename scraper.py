import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

class Vanguard(object):

    def __init__(self):
        self.ASUU_articles = []
        self.titles = []
        self.summary = []
        self.links = []
        self.time = []

        for page_number in range(1, 4):
            self.get_ASUU_articles(page_number)

    def get_ASUU_articles(self, page_number):
        page_content = requests.get("https://www.vanguardngr.com/news/page/{}".format(page_number)).content
        parsed_page_content = bs(page_content, "html.parser")
        articles = parsed_page_content.find_all("article")
        for article in articles:
            if "asuu" in article.find_all("a")[1].text.lower():
                self.ASUU_articles.append(article)

    def get_titles(self):
        for article in self.ASUU_articles:
            self.titles.append(article.find_all("a")[1].text)

    def get_summary(self):
        for article in self.ASUU_articles:
            self.summary.append(article.find("div", {"class": "entry-content"}).text.split["Read more"][0])

    def get_links(self):
        for article in self.ASUU_articles:
            self.links.append(article.find("a")["href"])

    def get_post_times(self):
        for link in self.links:
            page_content = requests.get(link).content
            parsed_page_content = bs(page_content, "html.parser")
            time = parsed_page_content.find("meta", {"property": "article:published_time"})["content"]
            time_format = "%Y-%m-%dT%H:%M:%S"
            parsed_time = time.split("+")[0]
            self.time.append(datetime.strptime(parsed_time, time_format))

class TheNation(object):

    def __init__(self):
        self.ASUU_articles = []
        self.titles = []
        self.summary = []
        self.links = []
        self.time = []

        for page_number in range(1, 4):
            self.get_ASUU_articles(page_number)

    def get_ASUU_articles(self, page_number):
        page_content = requests.get("http://thenationonlineng.net/category/news-update/page/{}".format(page_number)).content
        parsed_page_content = bs(page_content, "html.parser")
        articles = parsed_page_content.find_all("article")
        for article in articles:
            if "asuu" in article.find_all("a")[1].text.lower():
                self.ASUU_articles.append(article)

    def get_titles(self):
        for article in self.ASUU_articles:
            self.titles.append(article.find("a").text)

    def get_summary(self):
        for article in self.ASUU_articles:
            self.summary.append(article.find("div", {"class": "archive-content"}).text.split["Read More"][0])

    def get_links(self):
        for article in self.ASUU_articles:
            self.links.append(article.find("a")["href"])

    def get_post_times(self):
        for link in self.links:
            page_content = requests.get(link).content
            parsed_page_content = bs(page_content, "html.parser")
            time = parsed_page_content.find("meta", {"property": "article:published_time"})["content"]
            time_format = "%Y-%m-%dT%H:%M:%S"
            parsed_time = time.split("+")[0]
            self.time.append(datetime.strptime(parsed_time, time_format))

