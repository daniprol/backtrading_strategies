import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from strategies.stochastic_SMA_WMA import SMA_WMA
from strategies.MAC_EMA import MAC_EMA
from strategies.parabolic import Parabolic
from strategies.SMA_crossover import SmaCross
from backtesting import Strategy, Backtest
import yfinance as yf

ticker = 'BTC-USD'
data = yf.download(ticker, start="2020-01-01", end="2021-04-30")

# bt = Backtest(data, MAC_EMA, cash=1000000, commission=.002, exclusive_orders=True)
# bt = Backtest(data, SMA_WMA, cash=1000000, commission=.002, exclusive_orders=True)
# bt = Backtest(data, Parabolic, cash=1000000, commission=.002, exclusive_orders=True)
bt = Backtest(data, SmaCross, cash=1000000, commission=.002, exclusive_orders=True)
output = bt.run()
print(output)
bt.plot()


# OPTIMIZATION MAC_EMA, stochastic SMA_WMA
# stats, heatmap = bt.optimize(profit_short = range(90,99,1), profit = range(101,110,1), stop_loss=range(90,99,1),
#     stop_loss_short=range(101,110,1),  maximize='Equity Final [$]',return_heatmap=True)
# print(stats)
# print(stats._strategy)
# hm = heatmap.groupby(['profit', 'profit_short','stop_loss','stop_loss_short']).mean().unstack()
# print(heatmap.sort_values(ascending=False).iloc[:10])
# plt.figure(figsize=(12, 10))
# sns.heatmap(hm[::-1], cmap='viridis')
# plt.savefig('MAC_EMA_optimization.png')
# bt.plot()



# OPTIMIZATION PARABOLIC
# stats, heatmap = bt.optimize(d_rsi=range(10, 35, 5), w_rsi=range(10, 35, 5), \
#                              level=range(30, 80, 10), return_heatmap=True)
# print(stats)
# hm = heatmap.groupby(['d_rsi', 'w_rsi', 'level']).mean().unstack()
# print(heatmap.sort_values(ascending=False).iloc[:10])
# plt.figure(figsize=(12, 10))
# sns.heatmap(hm[::-1], cmap='viridis')
# plt.savefig('foo.png')
# bt.plot()


# OPTIMIZE SMA_crossover
stats,heatmap = bt.optimize(n1=range(5, 120, 5),\
     n2=range(20, 220, 5), maximize='Equity Final [$]', \
    constraint=lambda param: param.n1 < param.n2, return_heatmap=True)
print(stats)
print(stats._strategy)
bt.plot()
print(heatmap.sortvalues(ascending=False).iloc[:10])
hm = heatmap.groupby(['n1', 'n2']).mean().unstack()
plt.figure(figsize=(12, 10))
sns.heatmap(hm[::-1], cmap='viridis')
plt.savefig('sma-cross-heatmap.png')
