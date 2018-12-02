import requests
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime

class Vanguard(object):
    """
    Parses news from the vanguard website: https://www.vanguardngr.com/news
    """

    def __init__(self):
        self.ASUU_news = []
        self.titles = []
        self.summary = []
        self.links = []
        self.time = []

        for page_number in range(1, 3):
            self.get_ASUU_news(page_number)

    def get_ASUU_news(self, page_number):
        """
        Checks for each news in "news box".
        Then appends the content to the self.ASUU_articles list
        if the keyword "asuu" exists in the news title.
        :param page_number: int
        :return: None
        """
        page = requests.get("https://www.vanguardngr.com/news/page/{}".format(page_number)).content
        parsed_page = bs(page, "html.parser")
        news = parsed_page.find_all("article")
        for article in news:
            if "asuu" in article.find_all("a")[1].text.lower():
                self.ASUU_news.append(article)

    def get_titles(self):
        """
        Parses html to get the news titles
        :return: None
        """
        for article in self.ASUU_news:
            self.titles.append(article.find_all("a")[1].text)

    def get_summary(self):
        """
        Parses the "news box" and extracts the news snippet
        :return: None
        """
        for article in self.ASUU_news:
            unparsed_summary = article.find("div", {"class": "entry-content"}).text
            # Read more text in news snippet parsed out.
            parsed_summary = re.split(r"[Rr]ead [Mm]ore", unparsed_summary)[0]
            self.summary.append(parsed_summary)

    def get_links(self):
        """
        Parses the content of the "news box" and gets the link for each news
        :return: None
        """
        for article in self.ASUU_news:
            self.links.append(article.find("a")["href"])

    def get_post_times(self):
        """
        Gets the publish time for the news from the meta tag
        :return: None
        """
        for link in self.links:
            page_content = requests.get(link).content
            parsed_page_content = bs(page_content, "html.parser")
            time = parsed_page_content.find("meta", {"property": "article:published_time"})["content"]
            time_format = "%Y-%m-%dT%H:%M:%S"
            parsed_time = time.split("+")[0]
            self.time.append(datetime.strptime(parsed_time, time_format))


class PremiumTimes(object):
    """
    Parses news from the PremiumTimes website: https://www.premiumtimesng.com/category/news
    """

    def __init__(self):
        self.ASUU_news = []
        self.titles = []
        self.summary = []
        self.links = []
        self.time = []

        for page_number in range(1, 3):
            self.get_ASUU_news(page_number)

    def get_ASUU_news(self, page_number):
        """
        Checks for each news in "news box".
        Then appends the content to the self.ASUU_articles list
        if the keyword "asuu" exists in the news title.
        :param page_number:
        :return: None
        """
        page_content = requests.get("https://www.premiumtimesng.com/category/news/page/{}".format(page_number)).content
        parsed_page_content = bs(page_content, "html.parser")
        news = parsed_page_content.find_all("div", {"class": "a-story"})
        for article in news:
            if len(article.find_all("a")[2].findChildren()) == 0:
                continue
            if "asuu" in article.find_all("a")[2].find("h3").text.lower():
                self.ASUU_news.append(article)

    def get_titles(self):
        """
        Parses html to get the news titles
        :return: None
        """
        for article in self.ASUU_news:
            self.titles.append(article.find_all("a")[2].find("h3").text)

    def get_summary(self):
        """
        Visits each news link and parses the html.
        Gets the first two paragraphs from the news page.
        :return: None
        """
        self.get_links()
        unique_links = set(self.links)
        self.links = list(unique_links)
        for link in self.links:
            page = requests.get(link)
            parsed_page = bs(page.content, "html.parser")
            page_content = parsed_page.find("div", {"class": "entry-content manoj single-add-content"})
            paragraphs_tags = page_content.find_all("p")[:2]
            paragraph_text = [each.text for each in paragraphs_tags]
            parsed_summary = " ".join(paragraph_text)
            self.summary.append(parsed_summary)

    def get_links(self):
        """
        Parses the content of the "news box" and gets the link for each news
        :return: None
        """
        for article in self.ASUU_news:
            self.links.append(article.find_all("a")[2]["href"])

    def get_post_times(self):
        """
        Gets the publish time for the news from the meta tag
        :return: None
        """
        for link in self.links:
            page_content = requests.get(link).content
            parsed_page_content = bs(page_content, "html.parser")
            time = parsed_page_content.find("meta", {"property": "article:published_time"})["content"]
            time_format = "%Y-%m-%dT%H:%M:%S"
            parsed_time = time.split("+")[0]
            self.time.append(datetime.strptime(parsed_time, time_format))
