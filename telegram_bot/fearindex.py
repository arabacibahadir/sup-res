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
    text_fear = []
    for i in info:
        text_fear.append(i.text)
    return f"Fear&Greed Index:\nNow: {text_fear[0]}\nYesterday: {text_fear[1]}\n" \
           f"Last Week: {text_fear[2]}\nLast Month: {text_fear[3]}\n"

