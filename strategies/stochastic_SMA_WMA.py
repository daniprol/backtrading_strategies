import talib as talib
from datetime import datetime
from datetime import timedelta
from backtesting import Strategy, Backtest
from backtesting.lib import resample_apply


## Three indicators two time frames
# WMA(144),  SMA(5)
## hourly chart to look for direction of the trend
# SMA(5) < WMA(144) downtrend
# SMA(5) > WMA(144) uptrend
## 5 minute chart to make entries
# SMA(5) < WMA(144) downtrend
# SMA(5) > WMA(144) uptrend

class SMA_WMA(Strategy):
    n1 = 5
    n2 = 144
    level = 20
    profit = 106
    profit_short = 91
    stop_loss = 95
    long_short = 1
    level_short = 80
    stop_loss_short = 101
    buy_price = 0
    sell_price = 0

    def init(self):
        # Compute moving averages the strategy demands
        self.sma5 = self.I(talib.SMA, self.data.Close, self.n1)
        self.wma144 = self.I(talib.WMA, self.data.Close, self.n2)
        self.slowk, self.slowd = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close)
        self.hsma5 = resample_apply('H', talib.SMA, self.data.Close, self.n1)
        self.hwma144 = resample_apply('H', talib.WMA, self.data.Close, self.n2)
        # we will use this later with another stoploss strategy

    def next(self):
        price = self.data.Close[-1]
        # If we don't already have a position, and
        # if all conditions are satisfied, enter long.
        if (not self.position and
                self.slowk[-1] < self.level and
                self.slowd[-1] < self.level and
                self.slowk[-1] > self.slowd[-1] and
                self.sma5[-1] > self.wma144[-1] and
                self.hsma5[-1] > self.hwma144[-1]):
            self.buy(sl=self.stop_loss * price / 100)
            self.long_short = 1
            self.buy_price = price

        # If the price closes at our profit target
        # close the position, if any.
        elif (price > self.buy_price * self.profit / 100 and self.long_short == 1):
            self.position.close()
            self.long_short = 0
            self.buy_price = 0

        elif (not self.position and
              self.slowk[-1] > self.level_short and
              self.slowd[-1] > self.level_short and
              self.slowk[-1] > self.slowd[-1] and
              self.sma5[-1] < self.wma144[-1] and
              self.hsma5[-1] < self.hwma144[-1]):
            self.sell(sl=self.stop_loss_short * price / 100)
            self.long_short = 2
            self.sell_price = price

        # If the price closes at our profit target
        # close the position, if any.
        elif (price < self.sell_price * self.profit_short / 100 and self.long_short == 2):
            # elif (price > self.profit_short/100 * self.sma5[-1] and self.long_short == 2):
            # elif (price < price + 1.5*self.n_atr*self.atr[-1] and self.long_short == 2):
            self.position.close()
            self.long_short = 0
            self.sell_price = 0


# Optimization code
'''
stats, heatmap = bt.optimize(profit_short = range(90,99,1), profit = range(101,110,1), stop_loss=range(90,99,1), 
    stop_loss_short=range(101,110,1),  maximize='Equity Final [$]',return_heatmap=True)
print(stats)
print(stats._strategy)
hm = heatmap.groupby(['profit', 'profit_short','stop_loss','stop_loss_short']).mean().unstack()
print(heatmap.sort_values(ascending=False).iloc[:10])
plt.figure(figsize=(12, 10))
sns.heatmap(hm[::-1], cmap='viridis')
plt.savefig('foo.png')
bt.plot()
'''