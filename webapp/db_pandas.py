from binance.client import Client
import pandas as pd
import time

alarm_list = 'alarm1', 'alarm2', 'alarm3', 'alarm4', 'alarm5', 'alarm6', 'alarm7', 'alarm8', 'alarm9', 'alarm10', \
             'alarm_count'


def create_db():
    client = Client("", "")
    df = pd.DataFrame(client.get_all_tickers(), columns={'symbol': str(), 'price': float()})
    df.to_csv('api_data.csv', index=False)

    alarm_data_columns = {'symbol': str(), 'alarm1': float(), 'alarm2': float(), 'alarm3': float(), 'alarm4': float(),
                          'alarm5': float(), 'alarm6': float(), 'alarm7': float(), 'alarm8': float(), 'alarm9': float(),
                          'alarm10': float(), 'alarm_count': int()}
    alarm_data = pd.DataFrame(df['symbol'], columns=alarm_data_columns)
    for _ in alarm_list:
        alarm_data.fillna({_: 0}, inplace=True)
    alarm_data.to_csv('alarm_data.csv', index=False)


def get_live_price(self: str):
    df = pd.DataFrame(Client("", "").get_all_tickers(), columns={'symbol': str(), 'price': float()})
    coin = df.loc[df['symbol'] == self, ['symbol', 'price']]
    return print(coin.to_dict('records')[0]['price'])


def add_alarm_data(self: str, alarm: float):
    alarm_db = pd.read_csv('alarm_data.csv')
    coin = alarm_db.loc[alarm_db['symbol'] == self, ['symbol']]
    coin_dict = alarm_db[alarm_db['symbol'] == self].to_dict('records')[0]
    if alarm_db.at[coin.index[0], 'symbol'] == self:
        for i in alarm_list:
            if 0 not in coin_dict.values():
                return print("All alarms are full. Try to remove one alarm to add new one.")

            if alarm in coin_dict.values():
                return print(f"{self}: {alarm} is already exist in alarm_data")

            if coin_dict[i] == 0:
                alarm_db.at[coin.index[0], i] = alarm
                alarm_db.at[coin.index[0], 'alarm_count'] += 1
                alarm_db.to_csv('alarm_data.csv', index=False)
                return print(f"{self}: {alarm} added")

            if coin_dict[i] != 0:
                continue


def remove_alarm_data(self: str, alarm: float):
    alarm_db = pd.read_csv('alarm_data.csv')
    coin = alarm_db.loc[alarm_db['symbol'] == self, ['symbol']]
    for i in alarm_list:
        if alarm_db[alarm_db['symbol'] == self].to_dict('records')[0][i] == alarm:
            alarm_db.at[coin.index[0], i] = 0
            alarm_db.to_csv('alarm_data.csv', index=False)
            print(f"{self}: {alarm} removed")
            break


# TESTING
# create_db()
# get_live_price('BTCUSDT')
# add_alarm_data('BTCUSDT', 1000)
# add_alarm_data('ETHBTC', 3000)
# add_alarm_data('ETHBTC', 1000)
# add_alarm_data('ETHBTC', 2000)
# add_alarm_data('ETHBTC', 3003)
# add_alarm_data('ETHBTC', 3004)
# add_alarm_data('ETHBTC', 3005)
# add_alarm_data('ETHBTC', 3005)
# add_alarm_data('ETHBTC', 3022)
# add_alarm_data('ETHBTC', 3034)
# add_alarm_data('ETHBTC', 3067)
# add_alarm_data('ETHBTC', 3090)
# add_alarm_data('ETHBTC', 3007)
# add_alarm_data('ETHBTC', 3007)

# remove_alarm_data('ETHBTC', 2000)
# remove_alarm_data('BTCUSDT', 1000)
