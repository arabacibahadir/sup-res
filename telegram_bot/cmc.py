import requests
from bs4 import BeautifulSoup

text, news_all = [], []


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
    for a_href in soup.find_all("a", href=True):
        text.append(a_href.text)
    index = text.index("Headlines")
    for _ in text[index:index + 15:2]:
        news_all.append(_)
    news_list = ["-" + sub for sub in news_all]
    news_list.append(URL)
    return "\n".join(news_list)


def fear():
    """
    It scrapes the Fear&Greed Index from alternative.me
    :return: A string of Fear&Greed Index data to telegram-bot.
    """
    URL = "https://alternative.me/crypto/fear-and-greed-index/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    info = soup.find_all("div", class_="fng-circle")
    for i in info:
        text.append(i.text)
    return f"Fear&Greed Index:\nNow: {text[0]}\nYesterday: {text[1]}\n" \
           f"Last Week: {text[2]}\nLast Month: {text[3]}\n"
