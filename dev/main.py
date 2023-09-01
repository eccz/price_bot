import time
import threading
from binance_websocket_connector import run
from binance_websocket_connector import ggl_base_reader
from binance_websocket_connector import user_data
from binance_websocket_connector import binance_data
from binance_websocket_connector import comparator

if __name__ == '__main__':
    ws_thread = threading.Thread(target=run).start()
    ggs_thread = threading.Thread(target=ggl_base_reader).start()
    comp_thread = threading.Thread(target=comparator, args=(user_data, binance_data)).start()

    # test_thread = threading.Thread(target=thr_test).start()
