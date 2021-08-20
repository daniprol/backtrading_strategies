import datetime

import pandas as pd
import requests, json

base_url = "https://api.gemini.com/v1"
response = requests.get(base_url + "/symbols")
symbols = response.json()

print(symbols)


def get_candles_dataframe(json_data):
    candles_df = pd.DataFrame(json_data)
    candles_df.columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volumne"
    ]

    candles_df['time'] = candles_df['time'].apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1000)
    )

    return candles_df


btcusd_prices = get_candles_dataframe(response.json())
btcusd_prices.to_csv('BTCUSD', index=False)