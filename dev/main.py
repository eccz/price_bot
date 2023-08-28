import gspread
from dev import GS_GOOGLE_ALERT_SHEET
from dev import GS_KEY_FILE_NAME
from collections import namedtuple
import pandas as pd


def ggl_base_read(filename=GS_KEY_FILE_NAME, sht=GS_GOOGLE_ALERT_SHEET):
    gc = gspread.service_account(filename=filename)
    sht1 = gc.open_by_key(sht)
    worksheet = sht1.get_worksheet(0)

    result = []

    '''Через одиночные запросы - медленно'''
    # worksheet_size = len(worksheet.col_values(2)) - 1
    # for i in range(worksheet_size):
    #     ticker = namedtuple('ticker', ['name', 'condition', 'value'])
    #     ticker.name = worksheet.acell(f'B{i+2}').value
    #     ticker.condition = worksheet.acell(f'C{i+2}').value
    #     ticker.value = worksheet.acell(f'D{i+2}').value
    #     result.append(ticker)

    '''Через pandas быстрее, но городить pandas на ровном месте не хочется'''
    # dataframe = pd.DataFrame(worksheet.get_all_records())
    #
    # for i in dataframe.iterrows():
    #     ticker = namedtuple('ticker', ['name', 'condition', 'value'])
    #     ticker.name = i[1]['Тикер binance']
    #     ticker.condition = i[1]['Условие']
    #     ticker.value = i[1]['Стоимость']
    #
    #     result.append(ticker)

    for i in worksheet.get_all_records():
        ticker = namedtuple('ticker', ['name', 'condition', 'value', 'status'])
        ticker.name = i['Тикер binance']
        ticker.condition = i['Условие']
        ticker.value = i['Стоимость']
        ticker.status = i['Обрабатывается']

        result.append(ticker)

    return result


if __name__ == '__main__':
    a = ggl_base_read()
    # print([(i.name, i.value) for i in a])
