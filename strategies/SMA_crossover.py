import sqlite3 as sql
import pandas as pd
import numpy as np
import talib as talib
from datetime import datetime
from datetime import timedelta
from backtesting import Strategy, Backtest
from backtesting.lib import crossover
from matplotlib import pyplot as plt
import seaborn as sns


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        self.sma1 = self.I(talib.SMA, self.data.Close, self.n1)
        self.sma2 = self.I(talib.SMA, self.data.Close, self.n2)

    def next(self):
        # If sma1 crosses over sma2 buy
        if crossover(self.sma1, self.sma2):
            self.buy()
        # If sma1 crosses under sma2 sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()

