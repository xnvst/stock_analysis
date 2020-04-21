import sys

from alpha_vantage.timeseries import TimeSeries
import operator
import pandas as pd
import numpy
import talib

from datetime import datetime, timedelta

from quote_data import *
from plot import *
from pattern import *
from symbol_list import *

if __name__ == "__main__":
#    collect_all_quotes(append_new = 0)

    file = collect_quote('BA', append = 0)
    plot_candlestick(file)
#    quotes = pd.read_csv(file)
#    op = quotes['1. open']
#    hi = quotes['2. high']
#    lo = quotes['3. low']
#    cl = quotes['4. close']
#    upper, middle, lower = talib.BBANDS(cl, timeperiod=25)
#    upper.plot()
#    middle.plot()
#    lower.plot()
#    plt.show()
    sys.exit(0)

    for s in symbols:
        file = collect_quote(s, append = 0)
        if s == 'BA':
            plot_candlestick(file)
        date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
#       today = datetime.today().strftime('%Y-%m-%d')
        pattern_recognition(file, date)




