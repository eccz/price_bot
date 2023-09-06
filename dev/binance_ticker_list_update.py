from binance.spot import Spot as Client

import gspread
from dev import GS_GOOGLE_ALERT_SHEET
from dev import GS_KEY_FILE_NAME
from ggl_instruments import comma_string_to_float


def full_ticker_list():
    spot_client = Client()
    return [[i['symbol'], comma_string_to_float(i['price'])] for i in spot_client.ticker_price()]


def usdt_pairs_ticker_list():
    spot_client = Client()
    return [[i['symbol'], comma_string_to_float(i['price'])] for i in spot_client.ticker_price() if i['symbol'].endswith('USDT')]


def list_update(t_list):
    gc = gspread.service_account(filename=GS_KEY_FILE_NAME)
    sht1 = gc.open_by_key(GS_GOOGLE_ALERT_SHEET)

    binance_ticker_list = sht1.get_worksheet(2) # 5 for full, 2 for usdt pairs
    binance_ticker_list.clear()
    binance_ticker_list.update(t_list)


if __name__ == '__main__':
    # скрипт позволяет обновить список тикеров binance для проверки правильности заполнения таблицы google docs
    list_update(usdt_pairs_ticker_list())
    # list_update(full_ticker_list())
