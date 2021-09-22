# Settings
# Which ones available usdt,usd,btc based like
# if coin not available assert
exchange_name = 'Binance'
coin_name = 'BTC'
pair_name = 'USDT'
time_series = 'd'
full_filename = str(exchange_name + "_" + coin_name + pair_name + "_" + time_series + ".csv")
print(full_filename)
