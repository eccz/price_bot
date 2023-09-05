from logger import logger
import gspread
from dev import GS_GOOGLE_ALERT_SHEET
from dev import GS_KEY_FILE_NAME


google_auth = gspread.service_account(filename=GS_KEY_FILE_NAME)
google_sheet = google_auth.open_by_key(GS_GOOGLE_ALERT_SHEET)


def worksheet_status_updater(worksheet: gspread.Worksheet, cell: gspread.Cell, symbol: str) -> None:
    worksheet.update_cell(cell.row, cell.col + 3, 'нет')
    logger.info(f'Статус {symbol} изменен в листе {worksheet.title}')


def worksheet_row_validation(row: dict) -> bool:
    if row['Тикер'] and row['Условие'] and row['Стоимость'] and row['Обрабатывается'] == 'да':
        return True


def comma_string_to_float(value: str) -> float:
    return float(value.replace(',', '.'))


def worksheet_get_all_records(worksheet: gspread.Worksheet, asset_type: str) -> list:
    res = []
    for i in worksheet.get_all_records(numericise_ignore=[3]):
        if worksheet_row_validation(i):
            ticker = {
                'symbol': i['Тикер'],
                'type': asset_type,
                'sign': i['Условие'],
                'price': comma_string_to_float(i['Стоимость']),
                'status': i['Обрабатывается']
            }
            res.append(ticker)
    logger.info(f'Выполнен запрос к листу {worksheet.title}')
    return res


def ggl_status_changer(symbol: str, asset_type: str, sht1=google_sheet) -> None:
    if asset_type == 'crypto':
        worksheet = sht1.get_worksheet(0)
        cell = worksheet.find(symbol.upper())
        worksheet_status_updater(worksheet, cell, symbol)
        return
    if asset_type == 'funds':
        worksheet = sht1.get_worksheet(1)
        cell = worksheet.find(symbol.upper())
        worksheet_status_updater(worksheet, cell, symbol)


def ggl_base_read(sht1=google_sheet) -> list:
    worksheet_crypto = sht1.get_worksheet(0)
    worksheet_funds = sht1.get_worksheet(1)
    return (worksheet_get_all_records(worksheet_crypto, asset_type='crypto') +
            worksheet_get_all_records(worksheet_funds, asset_type='funds'))


if __name__ == '__main__':
    a = ggl_base_read()
    # [print(i.name, i.value) for i in a]
    print(a)
    # ggl_status_changer('SBER', asset_type='funds')
