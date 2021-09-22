# This is for updating and getting data.
# https://www.cryptodatadownload.com/data/
import requests
import settings
import urllib3


def download_data():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    coin_url = str('https://www.cryptodatadownload.com/cdd/' + settings.exchange_name + "_" + settings.coin_name + settings.pair_name + "_" + settings.time_series + ".csv")
    req = requests.get(coin_url, verify=False)
    open(settings.full_filename, 'wb').write(req.content)

