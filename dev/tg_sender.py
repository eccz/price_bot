from dev import TG_BOT_TOKEN, TG_CHAT_IDS
import requests
import time


def send_msg(msg):
    for _id in TG_CHAT_IDS:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={_id}&text={msg}"
        requests.get(url)
        # time.sleep(1)
        break


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
