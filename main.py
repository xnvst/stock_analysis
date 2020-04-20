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
    file = collect_quote('CRMD', append = 1)
    sys.exit(0)

#    collect_all_quotes()

    file = collect_quote('CRMD', append = 0)
    date = datetime.strftime(datetime.now() - timedelta(3), '%Y-%m-%d')
#    today = datetime.today().strftime('%Y-%m-%d')
    pattern_recognition(file, date)

#    for s in symbol_list:
#        file = collect_quote(s)
#        if s == 'NBEV':
#            plot_candlestick(file)




