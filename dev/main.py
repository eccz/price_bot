import time
import threading
from binance_instruments import run
from binance_instruments import ggl_base_reader
from binance_instruments import ti_thread
from binance_instruments import user_data
from binance_instruments import binance_data
from binance_instruments import comparator

if __name__ == '__main__':
    ws_thread = threading.Thread(target=run).start()
    ggs_thread = threading.Thread(target=ggl_base_reader).start()
    ti_thread = threading.Thread(target=ti_thread).start()
    comp_thread = threading.Thread(target=comparator).start()

    # test_thread = threading.Thread(target=thr_test).start()
