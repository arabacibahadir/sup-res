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


def news():
    URL = "https://coinmarketcap.com/headlines/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    t = []
    n = []
    append_str = "-"
    for a_href in soup.find_all("a", href=True):
        t.append(a_href.text)
    index = t.index("Headlines")
    for _ in t[index:index + 15:2]:
        n.append(_)
    n = [append_str + sub for sub in n]
    n.append(URL)
    return "\n".join(n)
