from alpha_vantage.timeseries import TimeSeries
import operator
import pandas as pd
import numpy as np
from pathlib import Path
import time

from symbol_list import *

def get_quotes(name, outputsize = 'compact'):
    key = 'B478G0MJQCKU8MKM'
    ts = TimeSeries(key, output_format='pandas')
    if outputsize == 'full':
        quotes, meta = ts.get_daily(symbol=name, outputsize='full')
    else:
        quotes, meta = ts.get_daily(symbol=name, outputsize='compact')
    return quotes

def write_csv(path, data):
    data.to_csv(path)

def append_csv(path, data):
    quotes = pd.read_csv(path)
    remove_duplicate_and_write(path, quotes, data)

def remove_duplicate_and_write(path, quotes, data):
    merge = []
    i = 0
    for index,row in data.iterrows():
        s1 = str(index)[0:10]
        if quotes['date'].str.contains(s1).any():
            data.drop(index, inplace=True)
            pass
    data.to_csv('tmp.csv')
    quotes2 = pd.read_csv('tmp.csv')
    quotes = (pd.concat([quotes2, quotes], axis=0, join='inner')).sort_values(by=['date'], ascending=False)
    quotes.to_csv(path, index=False)

def collect_quote(symbol, outputsize = 'compact', append = 0):
    if outputsize == 'full':
        symbol_file = 'data/' + symbol + '_full.csv'
    else:
        symbol_file = 'data/' + symbol + '.csv'

    if Path(symbol_file).is_file():
        if append == 1:
            data = get_quotes(symbol)
            print (symbol_file + " exist & append")
            append_csv(symbol_file, data)
        else:
            print (symbol_file + " exist")
    else:
        data = get_quotes(symbol)
        print (symbol_file + " created")
        write_csv(symbol_file, data)
    return symbol_file

def collect_all_quotes(append_new):
    cnt = 0
    for s in symbols:
#        if s < 'HD':
#            continue
        file = collect_quote(s, append = append_new)
        time.sleep(11)
        cnt = cnt + 1
