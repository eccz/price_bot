from binance_instruments import binance_data
from ggl_instruments import user_data, ggl_status_changer, user_data_status_changer
from ti_instruments import ti_data
import time
from tg_sender import send_msg
from logger import logger


def compare(sign: str, exchange_price: float, user_price: float, symbol: str) -> bool:
    try:
        if sign == '>' and exchange_price > user_price:
            return True
        if sign == '<' and exchange_price < user_price:
            return True
        if sign == '>=' and exchange_price >= user_price:
            return True
        if sign == '<=' and exchange_price <= user_price:
            return True
    except TypeError:
        logger.error(f'Невозможно сравнить значения по {symbol}')


def comparator():
    while True:
        if not user_data or not binance_data or not ti_data:
            time.sleep(3)
            continue
        for i in user_data[0]:
            user_symbol = i.get('symbol')
            asset_type = i.get('type')
            sign = i.get('sign')
            user_price = i.get('price')
            status = i.get('status')
            for n in binance_data[0]:
                if n.get('symbol') == user_symbol and status == 'да':
                    if compare(sign, n.get('price'), user_price, user_symbol):
                        send_msg(f'Цена на {user_symbol} {sign} {user_price}, текущая цена = {n.get("price")}',
                                 user_symbol)
                        ggl_status_changer(user_symbol, asset_type, sign, user_price)
                        user_data_status_changer(user_symbol, sign, user_price)
                    time.sleep(3)
            if ti_data[0]:
                for m in ti_data[0]:
                    if m.get('symbol') == user_symbol and status == 'да':
                        if compare(sign, m.get('price'), user_price, user_symbol):
                            send_msg(f'Цена на {user_symbol} {sign} {user_price}, текущая цена = {m.get("price")}',
                                     user_symbol)
                            ggl_status_changer(user_symbol, asset_type, sign, user_price)
                            user_data_status_changer(user_symbol, sign, user_price)
                        time.sleep(3)
        time.sleep(1)
