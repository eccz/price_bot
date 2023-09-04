import websocket
import json
import time
from controller import ggl_base_read
from controller import ggl_status_changer
from controller import alert


result = []
user_data = [{}]
binance_data = [{}]
done_alerts = []


def comparator():
    while True:
        if user_data == [{}] or binance_data == [{}]:
            time.sleep(3)
            continue
        for i in user_data[0]:
            # print(user_data[0])
            if i in done_alerts: continue
            user_symbol = i.get('symbol')
            sign = i.get('sign')
            user_price = i.get('price')
            status = i.get('status')
            for n in binance_data[0]:
                if n.get('symbol') == user_symbol and status == 'да':
                    alert(user_symbol, sign, n.get('price'), user_price)
                    ggl_status_changer(user_symbol)
                    done_alerts.append(i)
                    time.sleep(2)
        time.sleep(1)


def ggl_base_reader():
    while True:
        time.sleep(5)
        user_data[0] = ggl_base_read()


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
