import asyncio
import json
import os
from websockets import connect
from datetime import datetime

websocket_url = "wss://fstream.binance.com/ws/!forceOrder@arr"
filename = "binance_force_orders.csv"

if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write(
            ",".join(
                [
                    "symbol",
                    "side",
                    "order_type",
                    "time_in_force",
                    "original_quantity",
                    "price",
                    "average_price",
                    "order_status",
                    "order_last_filled_quantity",
                    "order_filled_accumulated_quantity",
                    "order_trade_time",
                ]
            )
            + "\n"
        )


async def f_liqs(uri, filename):
    async for websocket in connect(uri):
        try:
            while True:
                msg = await websocket.recv()
                print(msg + "\n" + str(datetime.now()))
                msg = [str(x) for x in list(json.loads(msg)["o"].values())]
                with open(filename, "a") as m:
                    m.write(",".join(msg) + "\n")
        except Exception as e:
            print(e)
            continue


asyncio.run(f_liqs(websocket_url, filename))
