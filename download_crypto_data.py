import pandas as pd
# Needed to use unverified SSL
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# For example: BTC/USD data
url = "https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv"
url = "https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_1h.csv"
url = "https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_minute.csv"
df = pd.read_csv(url, delimiter=",", skiprows=[0])
print(df)

