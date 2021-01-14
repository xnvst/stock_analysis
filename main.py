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

    if 0:
        s = 'AAPL'
        technical_analysis(s)
        sys.exit(0)

    cnt = 0
    technical_list = []
    for s in my_symbols:
        if s != 'LLIT' and s != 'AAPL':
            continue

        # step 1 - collect quote
        if 0:
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
            t1, t2, t3 = technical_analysis(s)
            technical_list.append((s, t1, t2, t3))
            print('###----------------------------------------\n\n')

    technical_list.sort(key = (lambda elem : (elem[1], elem[2], elem[3])), reverse=True)
    print("symbol, macd, price_volume, mfi\n")
    for x in range(len(technical_list)):
        print(technical_list[x])

#    quotes = pd.read_csv("./nasdaq.csv")
#    for s in quotes["Symbol"]:
#        print("'" + s + "',")

#    file = collect_quote('AC.TO', outputsize = 'full', append = 1)
#    plot_candlestick(file)
#    sys.exit(0)

    print('bye! ^_^\n')


'''
选票基础价量关系，K线位阶，图形结构，资金辅助增加胜率，先考虑大资金的态度，再看中小资金是否跟风
'''
