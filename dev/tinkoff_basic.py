import os
import gspread
from pandas import DataFrame
import time

from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal

from dev import GS_KEY_FILE_NAME
from dev import GS_TI_BASE_SHEET

TOKEN = os.getenv('INVEST_TOKEN')

gc = gspread.service_account(filename=GS_KEY_FILE_NAME)

sht1 = gc.open_by_key(GS_TI_BASE_SHEET)


def get_price_by_figi(figi='BBG004730ZJ9'):
    """Example - How to create takeprofit buy order."""
    with Client(TOKEN) as client:
        # BBG004730ZJ9 - VTBR / BBG004730N88 - SBER

        # getting the last price for instrument
        last_price = (
            client.market_data.get_last_prices(figi=[figi]).last_prices[0].price
        )
        return quotation_to_decimal(last_price).to_eng_string()


def instrument_find_query():
    with Client(TOKEN) as client:
        r = client.instruments.find_instrument(query={'ticker': "SBER"})

        for i in r.instruments:
            print(i)


def figi_for_ticker():
    """Example - How to get figi by name of ticker."""

    ticker = "SBER"  # "BRH3" "SBER" "VTBR"

    with Client(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        tickers = []
        count = 0
        for method in ["shares", "bonds", "etfs", "currencies", "futures"]:
            for item in getattr(instruments, method)().instruments:
                tickers.append(
                    {
                        "name": item.name,
                        "ticker": item.ticker,
                        "class_code": item.class_code,
                        "figi": item.figi,
                        "uid": item.uid,
                        "type": method,
                        "currency": item.currency,
                        "exchange": item.exchange,
                        "last_price": get_price_by_figi(item.figi)
                    }
                )
                count += 1
                print(count)
                if count == 290:
                    time.sleep(60)
                    count = 0

        tickers_df = DataFrame(tickers)
        # a = [i for i in tickers_df.values]
        sht1.sheet1.clear()
        sht1.sheet1.update([tickers_df.columns.values.tolist()] + tickers_df.values.tolist(), 'A1')

        # ticker_df = tickers_df[tickers_df["ticker"] == ticker]
        #
        # figi = ticker_df["figi"].iloc[0]
        # uid = ticker_df["uid"].iloc[0]
        # print(f"\nTicker {ticker}, figi={figi}, uid={uid}")
        # print(f"Additional info for this {ticker} ticker:")
        # print(ticker_df.iloc[0])


if __name__ == '__main__':
    # get_price_by_figi(figi='BBG004730N88')
    figi_for_ticker()
    print('THE END')
    # with Client(TOKEN) as client:
    #     statuses = client.market_data.get_trading_statuses(instrument_ids=["BBG004730N88"])
    #     print(statuses)
