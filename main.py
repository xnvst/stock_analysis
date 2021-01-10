import sys

from alpha_vantage.timeseries import TimeSeries
import operator
import pandas as pd
import numpy

from datetime import datetime, timedelta

from quote_data import *
from plot import *
from pattern import *
from symbol_list import *
from technical import *

if __name__ == "__main__":
    print('welcome!\n')

    cnt = 0
    for s in my_symbols:
        # step 1 - collect quote
        if 1:
            file = collect_quote(s, append = 1, print_debug = 0)
            time.sleep(12)
            cnt = cnt + 1
            if cnt % 5 == 0:
                time.sleep(5)

        # step 2 - analysis
        if 1:
            print('\n\n$$$----------------------------------------')
            print(s)
            candle_pattern_recognition(s)
            macd_analysis(s)
            price_volume_analysis(s)
            print('###----------------------------------------\n\n')
            time.sleep(12)
            cnt = cnt + 1
            if cnt % 5 == 0:
                time.sleep(5)

#    quotes = pd.read_csv("./nasdaq.csv")
#    for s in quotes["Symbol"]:
#        print("'" + s + "',")

#    file = collect_quote('DLR.TO', outputsize = 'full', append = 1)
#    plot_candlestick(file)
#    sys.exit(0)

    print('bye! ^_^\n')



