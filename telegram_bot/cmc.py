import requests
from bs4 import BeautifulSoup


def market():
    """
    This function scrapes the market data from the coinmarketcap.com website and returns a string with
    the market data
    :return: A string of text.
    """
    URL = "https://coinmarketcap.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    info = soup.find("div", class_="cmc-global-stats__inner-content")
    text = []
    for i in info:
        text.append(i.text.replace('\xa0', ' '))
    return "\n".join(text)


def news():
    """
    The function returns a list of news headlines from the coinmarketcap.com website
    :return: A string of the news headlines.
    """
    URL = "https://coinmarketcap.com/headlines/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    text = []
    news = []
    for a_href in soup.find_all("a", href=True):
        text.append(a_href.text)
    index = text.index("Headlines")
    for _ in text[index:index + 15:2]:
        news.append(_)
    news = ["-" + sub for sub in news]
    news.append(URL)
    return "\n".join(news)
