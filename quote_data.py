from alpha_vantage.timeseries import TimeSeries
import operator
import pandas as pd
import numpy as np
from pathlib import Path
from symbol_list import *

def get_quotes(name, outputsize = 'compact', key_cnt = 0):
    ts = TimeSeries(key, output_format='pandas')
    try:
        if outputsize == 'full':
            quotes, meta = ts.get_daily(symbol=name, outputsize='full')
        else:
            quotes, meta = ts.get_daily(symbol=name, outputsize='compact')
    except:
        print("get_quotes exception")
    api_delay(key_cnt)
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

def collect_quote(symbol, outputsize = 'compact', append = 0, print_debug = 0, key_cnt = 0):
    if outputsize == 'full':
        symbol_file = 'data/' + symbol + '_full.csv'
    else:
        symbol_file = 'data/' + symbol + '.csv'

    if Path(symbol_file).is_file():
        if append == 1:
            data = get_quotes(symbol, outputsize, key_cnt)
            if print_debug == 1:
                print (symbol_file + " exist & append")
            append_csv(symbol_file, data)
        else:
            if print_debug == 1:
                print (symbol_file + " exist")
            pass
    else:
        data = get_quotes(symbol, outputsize, key_cnt)
        print (symbol_file + " created")
        write_csv(symbol_file, data)
    return symbol_file


