
import sqlite3 as sql
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
dbfile = 'bitcoin.db'
table = 'bitcoin_5minute_raw'
conn = sql.connect(dbfile)

start_date = '2021-05-01'
how_many_months = "-24"
SQL = "SELECT DISTINCT Date,Open,Close,Low,High,Volume_USD FROM " + \
      table + " WHERE Date < date('" + start_date + "') and Date > date('" + \
      start_date + "','start of month','" + how_many_months + \
      " month') ORDER BY Date"
print(SQL)

data = pd.read_sql(SQL, conn)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index("Date", inplace=True)
data.columns = ['Open', 'Close', 'Low', 'High', 'Volume'];

