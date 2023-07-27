import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient as Client
import json


# config_logging(logging, logging.DEBUG)

def message_handler(_, message):
    # logging.info(message)
    tmp = json.loads(message)
    if 's' in tmp:
        print(tmp["s"], tmp['c'])


my_client = Client(on_message=message_handler)

my_client.ticker(symbol="bnbusdt")

time.sleep(30)

logging.debug("closing ws connection")
my_client.stop()
