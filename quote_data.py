from alpha_vantage.timeseries import TimeSeries
import operator
import pandas as pd
from pathlib import Path

symbol_list = \
['SPYG', \
'AAOI', \
'BA', \
'NBEV', \
'CRMD', \
]


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
    remove_duplicate(quotes, data)
    write_csv(path, data)

def remove_duplicate(quotes, data):
    equal = []
    i = 0
    for index,row in data.iterrows():
        s1 = str(index)[0:10]
        s2 = str(quotes['date'][i])[0:10]
        print(s1 + "  " + s2)
        if (operator.eq(s1, s2)):
            equal.append(1)
            quotes.drop([i])
        else:
            equal.append(0)
            data = data.append(quotes[i])
        data = data.append(quotes)
        i = i + 1

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

def collect_all_quotes():
    for s in symbol_list:
        file = collect_quote(s, append = 1)
