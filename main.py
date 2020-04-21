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

if __name__ == "__main__":
    collect_all_quotes(append_new = 1)

#    date = datetime.strftime(datetime.now() - timedelta(3), '%Y-%m-%d')
#    today = datetime.today().strftime('%Y-%m-%d')
#    pattern_recognition(file, date)

#    for s in symbol_list:
#        file = collect_quote(s)
#        if s == 'NBEV':
#            plot_candlestick(file)




