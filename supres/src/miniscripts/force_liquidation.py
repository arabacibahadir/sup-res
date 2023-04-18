import asyncio
import json
import os
from websockets import connect
from datetime import datetime

"""
1000ms
{
    "e":"forceOrder",                   // Event Type
    "E":1568014460893,                  // Event Time
    "o":{
        "s":"BTCUSDT",                   // Symbol
        "S":"SELL",                      // Side
        "o":"LIMIT",                     // Order Type
        "f":"IOC",                       // Time in Force
        "q":"0.014",                     // Original Quantity
        "p":"9910",                      // Price
        "ap":"9910",                     // Average Price
        "X":"FILLED",                    // Order Status
        "l":"0.014",                     // Order Last Filled Quantity
        "z":"0.014",                     // Order Filled Accumulated Quantity
        "T":1568014460893,              // Order Trade Time

    }

}
"""

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
    """
    This is an asynchronous function that connects to a websocket URI, receives messages, prints them
    with a timestamp, extracts specific values from the messages, and writes them to a file.

    :param uri: The `uri` parameter is a string representing the WebSocket URI to connect to
    :param filename: The filename parameter is a string that represents the name of the file where the
    data received from the websocket will be written. The function f_liqs will append the data to this
    file
    """
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
