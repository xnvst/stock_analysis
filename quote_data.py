from alpha_vantage.timeseries import TimeSeries
import operator

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
        if (operator.eq(s1, s2)):
            equal.append(1)
        else:
            equal.append(0)
            data = data.append(row)
        i = i + 1

def collect_quote(symbol, outputsize = 'compact'):
    if outputsize == 'full':
        symbol_file = 'data/' + symbol + '_full.csv'
    else:
        symbol_file = 'data/' + symbol + '.csv'
    data = get_quotes('AAPL')
    write_csv(symbol_file, data)
    return symbol_file