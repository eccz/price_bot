import websocket
import json
import time
from collections import deque

binance_data = deque(maxlen=1)


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
        binance_data.append(res)


def run():
    stream_name = 'ALERTS'
    wss = 'wss://stream.binance.com:9443/ws/%s' % stream_name

    wsa = websocket.WebSocketApp(wss, on_message=on_message, on_open=on_open)
    wsa.run_forever()


if __name__ == '__main__':
    run()
