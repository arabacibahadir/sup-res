import requests
from bs4 import BeautifulSoup


def fear():
    """
    It scrapes the Fear&Greed Index from alternative.me
    :return: A string of Fear&Greed Index data.
    """
    URL = "https://alternative.me/crypto/fear-and-greed-index/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    info = soup.find_all("div", class_="fng-circle")
    t = []
    for i in info:
        t.append(i.text)
    return f"Fear&Greed Index:\nNow: {t[0]}\nYesterday: {t[1]}\nLast Week: {t[2]}\nLast Month: {t[3]}\n"

