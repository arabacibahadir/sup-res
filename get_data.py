# This is for updating and getting data.
# https://www.cryptodatadownload.com/data/binance/
import urllib3
import requests


def download_data():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    btc_url = 'https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv'
    r = requests.get(btc_url, verify=False)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    open('Binance_BTCUSDT_d.csv', 'wb').write(r.content)
