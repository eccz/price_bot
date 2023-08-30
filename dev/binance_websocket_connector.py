import websocket
import json

result = []


def on_open(_wsa):
    data = dict(
        method='SUBSCRIBE',
        id=1,
        params=['!miniTicker@arr']
    )

    _wsa.send(json.dumps(data))


def on_message(_wsa, data):
    # _ = json.loads(data)
    # for i in _:
    #     result.append(i['s']) if i['s'] not in result else None
    # print(len(result))
    print(json.loads(data))


def run():
    stream_name = 'ALERTS'
    wss = 'wss://stream.binance.com:9443/ws/%s' % stream_name

    wsa = websocket.WebSocketApp(wss, on_message=on_message, on_open=on_open)
    wsa.run_forever()


if __name__ == '__main__':
    run()
