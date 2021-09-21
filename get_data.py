# This is for updating and getting data.
# https://www.cryptodatadownload.com/data/
import urllib3
import requests
import settings


def download_data():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    coin_url = 'https://www.cryptodatadownload.com/cdd/' + settings.exchange_name + "_" + settings.coin_name + settings.pair_name + "_" + settings.time_series + ".csv"
    req = requests.get(coin_url, verify=False)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    open('Binance_BTCUSDT_d.csv', 'wb').write(req.content)

