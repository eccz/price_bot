import os

from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal
from logger import logger
from ggl_instruments import user_data
import time
from collections import deque

ti_data = deque(maxlen=1)


TOKEN = os.getenv('INVEST_TOKEN')

tmp = [{'symbol': 'VTBR', 'type': 'funds', 'sign': '>', 'price': 0.01, 'status': 'да'},
       {'symbol': 'RUAL', 'type': 'funds', 'sign': '<', 'price': 35.0, 'status': 'да'},
       {'symbol': 'FIVE', 'type': 'funds', 'sign': '>', 'price': 2100.0, 'status': 'да'}]


def dataset_validation(dataset: list) -> bool:
    try:
        if dataset[0].get('symbol') and any([i.get('type') == 'funds' for i in dataset]):
            logger.info('Проверка датасета ti_instrument прошла')
            return True
        else:
            logger.info('Проверка датасета ti_instrument не прошла')
    except IndexError as err:
        logger.error('user_data пустая')


def data_to_ticker_list(dataset):
    return [i.get('symbol') for i in dataset if i.get('type') == 'funds']


def figis_by_ticker(ticker_list):

    with Client(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        tickers = []
        for item in instruments.shares().instruments:
            tickers.append(
                {
                    "symbol": item.ticker,
                    "figi": item.figi
                }
            ) if item.ticker in ticker_list else None
    logger.info(f'Получено {len(tickers)} figi по списку тикеров')
    return tickers


def get_price_by_figi(figi_ticker_list):
    result = []
    figi_list = [i.get('figi') for i in figi_ticker_list]
    with Client(TOKEN) as client:
        last_prices = (
            client.market_data.get_last_prices(figi=figi_list).last_prices
        )

        for index, item in enumerate(last_prices):
            result.append(dict(
                symbol=figi_ticker_list[index].get('symbol'),
                figi=item.figi,
                price=float(quotation_to_decimal(item.price).to_eng_string()),
                time=item.time.ctime()
            ))
    logger.info(f'Получено {len(result)} цен по списку тикеров')
    return result


def ti_handler(dataset) -> list:
    if dataset_validation(dataset):
        ticker_list = data_to_ticker_list(dataset)
        figi_ticker_list = figis_by_ticker(ticker_list)
        return get_price_by_figi(figi_ticker_list)


def ti_worker():
    while True:
        time.sleep(4)
        data = ti_handler(user_data[0])
        ti_data.append(data)
        time.sleep(14)


if __name__ == '__main__':
    # get_price_by_figi(['BBG004730N88'])
    # get_price_by_figi(['BBG004730ZJ9', 'BBG00F6NKQX3', 'BBG004730N88'])
    print(figis_by_ticker(['AAPL', 'SBER']))
