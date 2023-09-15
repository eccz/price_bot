import os
import time
from tinkoff.invest.utils import quotation_to_decimal

from tinkoff.invest import (
    LastPriceInstrument,
    Client,
    MarketDataRequest,
    SubscribeLastPriceRequest,
    SubscriptionAction,
)

TOKEN = os.environ["INVEST_TOKEN"]


def main(figi_list):
    instruments = [LastPriceInstrument(figi) for figi in figi_list]

    def request_iterator():
        yield MarketDataRequest(
            subscribe_last_price_request=SubscribeLastPriceRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=instruments
            )
        )

        while True:
            time.sleep(1)

    with Client(TOKEN) as client:
        for marketdata in client.market_data_stream.market_data_stream(
                request_iterator()
        ):
            try:
                print(marketdata.last_price.figi, quotation_to_decimal(marketdata.last_price.price),
                      marketdata.last_price.time)
            except Exception as ex:
                ...


if __name__ == "__main__":
    main(figi_list=['BBG004730N88', 'BBG004730ZJ9', 'BBG00F6NKQX3'])
