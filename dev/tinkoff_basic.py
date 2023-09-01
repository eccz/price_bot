import os
import gspread
from pandas import DataFrame
import time

from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal

from dev import GS_KEY_FILE_NAME
from dev import GS_GOOGLE_ALERT_SHEET

TOKEN = os.getenv('INVEST_TOKEN')

gc = gspread.service_account(filename=GS_KEY_FILE_NAME)

sht1 = gc.open_by_key(GS_GOOGLE_ALERT_SHEET)


def get_price_by_figi(figi_list):
    result = []

    with Client(TOKEN) as client:
        last_prices = (
            client.market_data.get_last_prices(figi=figi_list).last_prices
        )

        for item in last_prices:
            result.append(dict(
                figi=item.figi,
                price=float(quotation_to_decimal(item.price).to_eng_string()),
                time=item.time.ctime()
            ))

    return result


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
        # sht1.sheet1.clear()
        worksheet = sht1.get_worksheet(3)
        worksheet.clear()
        worksheet.update([tickers_df.columns.values.tolist()] + tickers_df.values.tolist(), 'A1')

        # ticker_df = tickers_df[tickers_df["ticker"] == ticker]
        #
        # figi = ticker_df["figi"].iloc[0]
        # uid = ticker_df["uid"].iloc[0]
        # print(f"\nTicker {ticker}, figi={figi}, uid={uid}")
        # print(f"Additional info for this {ticker} ticker:")
        # print(ticker_df.iloc[0])


if __name__ == '__main__':
    a = get_price_by_figi(figi_list=['BBG004730N88', 'BBG004730ZJ9', 'BBG00F6NKQX3'])
    print(a)
    # figi_for_ticker()
    # print('THE END')
    # with Client(TOKEN) as client:
    #     statuses = client.market_data.get_trading_statuses(instrument_ids=["BBG004730N88"])
    #     print(statuses)
