from logger import logger
import gspread
from dev import GS_GOOGLE_ALERT_SHEET
from dev import GS_KEY_FILE_NAME
from tg_sender import send_msg


def alert(symbol, sign, exchange_price, user_price):
    if sign == '>' and exchange_price > user_price:
        send_msg(f'Цена на {symbol.upper()} > {user_price}')
    if sign == '<' and exchange_price < user_price:
        send_msg(f'Цена на {symbol.upper()} < {user_price}')


def ggl_status_changer(symbol, filename=GS_KEY_FILE_NAME, sht=GS_GOOGLE_ALERT_SHEET):
    gc = gspread.service_account(filename=filename)
    sht1 = gc.open_by_key(sht)
    worksheet = sht1.get_worksheet(0)
    cell = worksheet.find(symbol.upper())
    if cell:
        worksheet.update_cell(cell.row, cell.col + 3, 'нет')
        logger.info(f'Статус {symbol} изменен в таблице с криптой')
    else:
        worksheet = sht1.get_worksheet(1)
        cell = worksheet.find(symbol.upper())
        if cell:
            worksheet.update_cell(cell.row, cell.col + 3, 'нет')
            logger.info(f'Статус {symbol} изменен в таблице с фондой')


def ggl_base_read(filename=GS_KEY_FILE_NAME, sht=GS_GOOGLE_ALERT_SHEET):
    gc = gspread.service_account(filename=filename)
    sht1 = gc.open_by_key(sht)
    worksheet_crypto = sht1.get_worksheet(0)
    worksheet_funds = sht1.get_worksheet(1)

    result = []

    for i in worksheet_crypto.get_all_records(numericise_ignore=[3]):
        if all(i.values()):
            # ticker = namedtuple('ticker', ['name', 'condition', 'value', 'status'])
            ticker = dict()
            ticker['symbol'] = i['Тикер']
            ticker['sign'] = i['Условие']
            ticker['price'] = float((i['Стоимость'].replace(',', '.')))
            if i['Обрабатывается'] == 'да':
                ticker['status'] = i['Обрабатывается']
            else:
                continue
            result.append(ticker)
    logger.info('Выполнен запрос к листу с криптой')

    for e in worksheet_funds.get_all_records(numericise_ignore=[3]):
        if all(e.values()):
            # ticker = namedtuple('ticker', ['name', 'condition', 'value', 'status'])
            ticker = dict()
            ticker['symbol'] = e['Тикер']
            ticker['sign'] = e['Условие']
            ticker['price'] = float((e['Стоимость'].replace(',', '.')))
            if e['Обрабатывается'] == 'да':
                ticker['status'] = e['Обрабатывается']
            else:
                continue
            result.append(ticker)

    logger.info('Выполнен запрос к листу с фондой')

    return result


if __name__ == '__main__':
    a = ggl_base_read()
    # [print(i.name, i.value) for i in a]
    # print(a)
    # ggl_status_changer('SBER')
