import requests
from bs4 import BeautifulSoup


def market():
    URL = "https://coinmarketcap.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    info = soup.find("div", class_="cmc-global-stats__inner-content")
    t = []
    for i in info:
        t.append(i.text.replace('\xa0', ' '))

    return "\n".join(t)
