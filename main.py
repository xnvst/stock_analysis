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

    #step 1 - every night
    if 0:
        collect_all_quotes(append_new = 1)

    # step 2 - analysis every day
    if 1:
        cnt = 0
        for s in my_symbols:
            print('\n\n$$$----------------------------------------')
            print(s)
            candle_pattern_recognition(s)
            macd_analysis(s)
            time.sleep(12)
            cnt = cnt + 1
            if cnt % 5 == 0:
                time.sleep(12)
            print('###----------------------------------------\n\n')

    #macd_analysis('MA')

#    quotes = pd.read_csv("./nasdaq.csv")
#    for s in quotes["Symbol"]:
#        print("'" + s + "',")

#    file = collect_quote('MA', outputsize = 'full', append = 1)
#    plot_candlestick(file)
#    sys.exit(0)

    print('bye! ^_^\n')



