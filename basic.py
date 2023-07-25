import os

from pandas import DataFrame

from tinkoff.invest import Client, SecurityTradingStatus
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal


TOKEN = os.getenv('INVEST_TOKEN')


def get_price_by_figi(figi='BBG004730ZJ9'):
    """Example - How to create takeprofit buy order."""
    with Client(TOKEN) as client:
        # BBG004730ZJ9 - VTBR / BBG004730N88 - SBER

        # getting the last price for instrument
        last_price = (
            client.market_data.get_last_prices(figi=[figi]).last_prices[0].price
        )
        last_price = quotation_to_decimal(last_price)
        print(f"{figi}, last price = {last_price}")


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
                        "min_price_increment": quotation_to_decimal(
                            item.min_price_increment
                        ),
                        "scale": 9 - len(str(item.min_price_increment.nano)) + 1,
                        "lot": item.lot,
                        "trading_status": str(
                            SecurityTradingStatus(item.trading_status).name
                        ),
                        "api_trade_available_flag": item.api_trade_available_flag,
                        "currency": item.currency,
                        "exchange": item.exchange,
                        "buy_available_flag": item.buy_available_flag,
                        "sell_available_flag": item.sell_available_flag,
                        "short_enabled_flag": item.short_enabled_flag,
                        "klong": quotation_to_decimal(item.klong),
                        "kshort": quotation_to_decimal(item.kshort),
                    }
                )

        tickers_df = DataFrame(tickers)

        ticker_df = tickers_df[tickers_df["ticker"] == ticker]

        figi = ticker_df["figi"].iloc[0]
        uid = ticker_df["uid"].iloc[0]
        print(f"\nTicker {ticker}, figi={figi}, uid={uid}")
        print(f"Additional info for this {ticker} ticker:")
        print(ticker_df.iloc[0])


if __name__ == '__main__':
    # get_price_by_figi(figi='BBG004730N88')
    figi_for_ticker()
    # with Client(TOKEN) as client:
    #     statuses = client.market_data.get_trading_statuses(instrument_ids=["BBG004730N88"])
    #     print(statuses)
