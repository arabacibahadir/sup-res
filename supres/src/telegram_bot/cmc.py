import requests
from bs4 import BeautifulSoup


def market():
    """
    This function scrapes the market data from the coinmarketcap.com website
    and returns a string with the market data
    :return: Market info text
    """
    URL = "https://coinmarketcap.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    market_info = soup.find("div", class_="cmc-global-stats__inner-content")
    text = [i.text.replace("\xa0", " ") for i in market_info]
    return "\n".join(text)


def news():
    """
    The function returns a list of news headlines from the coinmarketcap.com website
    :return: A string of the news headlines.
    """
    URL = "https://coinmarketcap.com/headlines/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    news_elements = soup.find_all("a", class_="sc-1eb5slv-0", href=True)
    news_all = [e.text for e in news_elements]
    news_list = ["-" + sub for sub in news_all[:15:2]]
    news_list.append(URL)
    return "\n".join(news_list)


def fear():
    """
    It scrapes the Fear&Greed Index from alternative.me
    :return: A string of Fear&Greed Index data to telegram-bot.
    """
    URL = "https://alternative.me/crypto/fear-and-greed-index/"
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        info = soup.find_all("div", class_="fng-circle")
        text = [i.text for i in info]
        return (
            f"Fear&Greed Index:\nNow: {text[0]}\nYesterday: {text[1]}\n"
            f"Last Week: {text[2]}\nLast Month: {text[3]}\n"
        )
    except requests.exceptions.RequestException:
        return "Error retrieving Fear&Greed Index data."
