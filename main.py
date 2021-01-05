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
#    collect_all_quotes(append_new = 1)
#    sys.exit(0)

#    quotes = pd.read_csv("./nasdaq.csv")
#    for s in quotes["Symbol"]:
#        print("'" + s + "',")

#    file = collect_quote('NBEV', append = 1)
#    plot_candlestick(file)
#    sys.exit(0)

    for s in my_symbols:
        candle_pattern_recognition(s)




