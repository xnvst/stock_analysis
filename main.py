from alpha_vantage.timeseries import TimeSeries
import operator
import pandas as pd
import numpy
import talib

from quote_data import *
from plot import *

symbol_list = \
['SPYG', \
'AAOI', \
'BA', \
'NBEV', \
'CRMD', \
]

if __name__ == "__main__":
    for s in symbol_list:
        file = collect_quote(s)
        if s == 'NBEV':
            plot_candlestick(file)




