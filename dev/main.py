import threading
from binance_instruments import run
from ggl_instruments import ggl_base_reader
from ti_instruments import ti_worker
from comparator import comparator

if __name__ == '__main__':
    ws_thread = threading.Thread(target=run).start()
    ggs_thread = threading.Thread(target=ggl_base_reader).start()
    ti_thread = threading.Thread(target=ti_worker).start()
    comp_thread = threading.Thread(target=comparator).start()
