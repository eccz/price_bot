import websocket
import json
import time
from ggl_instruments import ggl_base_read
from ggl_instruments import ggl_status_changer
from tg_sender import send_msg
from logger import logger
from ti_instruments import ti_handler

user_data = [{}]
binance_data = [{}]
ti_data = [{}]


def compare(sign: str, exchange_price: float, user_price: float) -> bool:
    if sign == '>' and exchange_price > user_price:
        return True
    if sign == '<' and exchange_price < user_price:
        return True
    if sign == '>=' and exchange_price >= user_price:
        return True
    if sign == '<=' and exchange_price <= user_price:
        return True


def user_data_status_changer(dataset: list, symbol: str, sign: str, user_price: float) -> None:
    for i in dataset[0]:
        if i.get('symbol') == symbol and i.get('sign') == sign and i.get('price') == user_price:
            i['status'] = 'нет'
            logger.info(f'Статус {symbol} в user_data изменен на нет')


def comparator():
    while True:
        if user_data == [{}] or binance_data == [{}] or ti_data == [{}]:
            time.sleep(3)
            continue
        for i in user_data[0]:
            user_symbol = i.get('symbol')
            asset_type = i.get('type')
            sign = i.get('sign')
            user_price = i.get('price')
            status = i.get('status')
            # if binance_data is not None:
            for n in binance_data[0]:
                if n.get('symbol') == user_symbol and status == 'да':
                    if compare(sign, n.get('price'), user_price):
                        send_msg(f'Цена на {user_symbol} {sign} {user_price}, текущая цена = {n.get("price")}', user_symbol)
                        ggl_status_changer(user_symbol, asset_type, sign, user_price)
                        user_data_status_changer(user_data, user_symbol, sign, user_price)
                    time.sleep(3)
            if ti_data[0] is not None:
                for m in ti_data[0]:
                    if m.get('symbol') == user_symbol and status == 'да':
                        if compare(sign, m.get('price'), user_price):
                            send_msg(f'Цена на {user_symbol} {sign} {user_price}, текущая цена = {m.get("price")}', user_symbol)
                            ggl_status_changer(user_symbol, asset_type, sign, user_price)
                            user_data_status_changer(user_data, user_symbol, sign, user_price)
                        time.sleep(3)
        time.sleep(1)


def ti_thread():
    while True:
        time.sleep(5)
        ti_data[0] = ti_handler(user_data[0])
        time.sleep(15)


def ggl_base_reader():
    while True:
        user_data[0] = ggl_base_read()
        time.sleep(20)


def on_open(_wsa):
    data = dict(
        method='SUBSCRIBE',
        id=1,
        params=['!miniTicker@arr']
    )

    _wsa.send(json.dumps(data))


def on_message(_wsa, data):
    tmp = json.loads(data)
    if tmp[0].get('e') is not None:
        res = [dict(symbol=e.get('s'), price=float(e.get('c')), time=time.ctime(e.get('E') / 1000)) for e in tmp]
        binance_data[0] = res


def run():
    stream_name = 'ALERTS'
    wss = 'wss://stream.binance.com:9443/ws/%s' % stream_name

    wsa = websocket.WebSocketApp(wss, on_message=on_message, on_open=on_open)
    wsa.run_forever()


if __name__ == '__main__':
    run()
