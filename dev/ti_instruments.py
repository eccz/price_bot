import os
from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal
from logger import logger

TOKEN = os.getenv('INVEST_TOKEN')

tmp = [{'symbol': 'VTBR', 'type': 'funds', 'sign': '>', 'price': 0.01, 'status': 'да'},
       {'symbol': 'RUAL', 'type': 'funds', 'sign': '<', 'price': 35.0, 'status': 'да'},
       {'symbol': 'FIVE', 'type': 'funds', 'sign': '>', 'price': 2100.0, 'status': 'да'}]


def dataset_validation(dataset: list) -> bool:
    if dataset[0].get('symbol'):
        return True


def data_to_ticker_list(dataset):
    return [i.get('symbol') for i in dataset]


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
    print(tickers)
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


if __name__ == '__main__':
    # get_price_by_figi(['BBG004730N88'])
    # get_price_by_figi(['BBG004730ZJ9', 'BBG00F6NKQX3', 'BBG004730N88'])
    print(ti_handler(tmp))
