from binance.spot import Spot as Client

import gspread
from dev import GS_GOOGLE_ALERT_SHEET
from dev import GS_KEY_FILE_NAME


def ticker_list():
    spot_client = Client()
    return [[i['symbol'], i['price']] for i in spot_client.ticker_price()]


def list_update():
    gc = gspread.service_account(filename=GS_KEY_FILE_NAME)
    sht1 = gc.open_by_key(GS_GOOGLE_ALERT_SHEET)

    worksheet2 = sht1.get_worksheet(1)
    worksheet2.clear()
    worksheet2.update(ticker_list())


if __name__ == '__main__':
    # скрипт позволяет обновить список тикеров binance для проверки правильности заполнения таблицы google docs
    list_update()
