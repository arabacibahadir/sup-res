import requests
from bs4 import BeautifulSoup
import settings
import urllib3

URL = 'https://www.cryptodatadownload.com/data/poloniex'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
page = requests.get(URL, verify=False)

soup = BeautifulSoup(page.text, "html.parser")
soup = str(soup.find_all("b"))
results = soup.replace('<b>', '').replace('</b>', '').replace('[', '').replace(']', '').replace(' ', '')


def convert(string):
    return list(string.split(","))


print(results)
# list_results = convert(results)

# for i in list_results:
#     print(i)
