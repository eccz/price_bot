from creds import TG_BOT_TOKEN
from creds import TG_CHAT_IDS  # list of id's ['123123', '345345345', '567567']
import requests
from logger import logger
import time


def send_msg(msg, symbol):
    for _id in TG_CHAT_IDS:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={_id}&text={msg}"
        requests.get(url)
        logger.info(f'Сообщение по тикеру {symbol} на ID {_id} отправлено')
        # time.sleep(1)
        break


def send_debug_msg(msg):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id=374543333&text={msg}"
    requests.get(url)
    logger.info(f'Debug message sent')


def bot_update():
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates"
    upd = requests.get(url).json()
    # print(upd)
    for i in upd['result']:
        print(i['message']['from']['first_name'], i['message']['from'].get('last_name'), i['message']['from']['id'])
        print(i['message']['text'], '\n')


if __name__ == '__main__':
    # send_msg(msg="ПРИВЕТ, БРАТ")
    bot_update()
