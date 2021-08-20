from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import talib as talib


class MAC_EMA(Strategy):
    stop_loss = 95
    profit = 109
    stop_loss_short = 104
    profit_short = 97
    long_short = 0
    buy_price = 0
    sell_price = 0

    def init(self):
        self.macd, self.macdsignal, self.macdhist = self.I(talib.MACD, self.data.Close, fastperiod=12, slowperiod=26,
                                                           signalperiod=9)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200)

    def next(self):
        price = self.data.Close[-1]
        if (not self.position and
                price > self.ema200[-1] and
                crossover(self.macd, self.macdsignal) and
                self.macd[-1] < 0 and self.macdsignal[-1] < 0):
            self.buy(sl=price * self.stop_loss / 100)
            self.buy_price = price
            self.long_short = 1
        elif (price > self.buy_price * self.profit / 100 and self.long_short == 1):
            self.position.close()
            self.long_short = 0
        elif (not self.position and
              price < self.ema200[-1] and
              crossover(self.macdsignal, self.macd) and
              self.macd[-1] > 0 and self.macdsignal[-1] > 0):
            self.sell(sl=price * self.stop_loss_short / 100)
            self.sell_price = price
            self.long_short = 2
        elif (price < self.sell_price * self.profit_short / 100 and self.long_short == 2):
            self.position.close()
            self.long_short = 0
            self.sell_price = 0

