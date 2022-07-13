from binance.client import Client
import pandas as pd
import time

alarm_list = 'alarm1', 'alarm2', 'alarm3', 'alarm4', 'alarm5', \
             'alarm6', 'alarm7', 'alarm8', 'alarm9', 'alarm10'


def create_db():
    client = Client("", "")
    df = pd.DataFrame(client.get_all_tickers(), columns={'symbol': str(), 'price': float()})
    df.to_csv('api_data.csv', index=False)

    alarm_data_columns = {'symbol': str(), 'alarm_count': int(), 'alarm1': float(), 'alarm2': float(),
                          'alarm3': float(), 'alarm4': float(), 'alarm5': float(), 'alarm6': float(),
                          'alarm7': float(), 'alarm8': float(), 'alarm9': float(), 'alarm10': float()}
    alarm_data = pd.DataFrame(df['symbol'], columns=alarm_data_columns)
    alarm_data.fillna({'alarm_count': 0}, inplace=True)
    alarm_data.update(alarm_data.fillna(0))
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


# shift alarm to left until there is no zero alarm
def shift_alarm(self: str):
    alarm_db = pd.read_csv('alarm_data.csv')
    coin = alarm_db.loc[alarm_db['symbol'] == self, ['symbol']]
    for i in alarm_list:
        if alarm_db[alarm_db['symbol'] == self].to_dict('records')[0][i] == 0:
            continue
        else:
            for j in alarm_list:
                if alarm_db[alarm_db['symbol'] == self].to_dict('records')[0][j] == 0:
                    alarm_db.at[coin.index[0], j] = alarm_db[alarm_db['symbol'] == self].to_dict('records')[0][i]
                    alarm_db.at[coin.index[0], i] = 0
                    alarm_db.to_csv('alarm_data.csv', index=False)
                    break


def remove_alarm_cell(self: str, alarm: float):
    alarm_db = pd.read_csv('alarm_data.csv')
    coin = alarm_db.loc[alarm_db['symbol'] == self, ['symbol']]
    for i in alarm_list:
        if alarm_db[alarm_db['symbol'] == self].to_dict('records')[0][i] == alarm:
            alarm_db.at[coin.index[0], i] = 0
            alarm_db.to_csv('alarm_data.csv', index=False)
            print(f"{self}: {alarm} removed")
            alarm_db.at[coin.index[0], 'alarm_count'] -= 1
            alarm_db.to_csv('alarm_data.csv', index=False)
            shift_alarm(self)
            break


def remove_all_alarms(self: str):
    alarm_db = pd.read_csv('alarm_data.csv')
    coin = alarm_db.loc[alarm_db['symbol'] == self, ['symbol']]
    for i in alarm_list:
        alarm_db.at[coin.index[0], i] = 0
        alarm_db.to_csv('alarm_data.csv', index=False)
        print(f"{self}: all alarms removed")
        break


def get_alarm_count():
    alarm_db = pd.read_csv('alarm_data.csv')
    for cell in alarm_db['alarm_count']:
        if cell != 0:
            symbol = alarm_db[alarm_db['alarm_count'] == cell]['symbol'].values[0]
            print(f"{symbol}: {cell}")


# TESTING
# create_db()
# get_live_price('BTCUSDT')
# shift_alarm('ETHBTC')
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
# get_alarm_count()
# remove_alarm_cell('ETHBTC', 2000)
# remove_alarm_cell('BTCUSDT', 1000)
# remove_all_alarms('BTCUSDT')
