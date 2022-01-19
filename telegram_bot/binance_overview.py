import requests
from bs4 import BeautifulSoup

URL = "https://www.binance.com/en/markets/overview"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")


def market():
    pcd = soup.find("div", class_="css-13dog1p")
    t = []
    for i in pcd:
        t.append(i.text)

    return f"Price Change Distribution All Coins:\n{t[0]}\n{t[1]}"


