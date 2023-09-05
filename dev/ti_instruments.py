import datetime

from pandas import DataFrame
import os
from tinkoff.invest import Client, SecurityTradingStatus
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal
from logger import logger

TOKEN = os.getenv('INVEST_TOKEN')

tmp = [{'symbol': 'VTBR', 'type': 'funds', 'sign': '>', 'price': 0.01, 'status': 'да'},
       {'symbol': 'RUAL', 'type': 'funds', 'sign': '<', 'price': 35.0, 'status': 'да'},
       {'symbol': 'FIVE', 'type': 'funds', 'sign': '>', 'price': 2100.0, 'status': 'да'}]


def data_to_ticker_list(dataset):
    return [i.get('symbol') for i in dataset]


def figis_by_ticker(ticker_list):
    """Example - How to get figi by name of ticker."""

    if ticker_list is None:
        ticker_list = ["APA", "BRH3", "SBER", "VTBR"]

    with Client(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        tickers = []
        start = datetime.datetime.now()
        print('start')
        for item in instruments.shares().instruments:
            tickers.append(
                {
                    "ticker": item.ticker, "figi": item.figi,
                    'type': 'shares',
                    "currency": item.currency,
                    "exchange": item.exchange
                }
            ) if item.ticker in ticker_list else None

    print(datetime.datetime.now() - start)
    return tickers


def get_price_by_figi(figi_list):
    result = []

    with Client(TOKEN) as client:
        last_prices = (
            client.market_data.get_last_prices(figi=figi_list).last_prices
        )

        for item in last_prices:
            print(item)
            result.append(dict(
                figi=item.figi,
                price=float(quotation_to_decimal(item.price).to_eng_string()),
                time=item.time.ctime()
            ))

    return result


if __name__ == '__main__':
    print(figis_by_ticker(None))
