from alpha_vantage.timeseries import TimeSeries

import operator

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick_ohlc

import numpy
import talib

def get_quotes(name):
    key = 'B478G0MJQCKU8MKM'
    ts = TimeSeries(key, output_format='pandas')
    #quotes, meta = ts.get_daily(symbol=name, outputsize='compact')
    quotes, meta = ts.get_daily(symbol=name, outputsize='full')

    #print(quotes['2020-02-07'])
    #print(quotes)
    #quotes.to_csv("aapl.csv")
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
        #print("index: " + s1)
        #print("quotes: " + s2)
        if (operator.eq(s1, s2)):
            #print("equal: " + s2)
            equal.append(1)
        else:
            equal.append(0)
            data = data.append(row)
        i = i + 1

def plot_candlestick(path):
    quotes = pd.read_csv(path)
    quotes.index = pd.to_datetime(quotes['date'])
    #print(quotes.index)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    # ax.xaxis.set_major_locator(mondays)
    #ax.xaxis.set_minor_locator(alldays)
    # ax.xaxis.set_major_formatter(weekFormatter)
    # ax.xaxis.set_minor_formatter(dayFormatter)
    # plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),quotes['1. open'], quotes['2. high'],quotes['3. low'], quotes['4. close']),width=0.6,colorup='r', colordown='g')
    ax.xaxis_date()
    #ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    _open = pd.to_datetime(quotes['1. open'])
    high = pd.to_datetime(quotes['2. high'])
    low = pd.to_datetime(quotes['3. low'])
    close = pd.to_datetime(quotes['4. close'])
    volume = pd.to_datetime(quotes['5. volume'])

    output = talib.SMA(close)
    real = talib.AD(high, low, close, volume)
    integer = talib.CDL2CROWS(_open, high, low, close)

    plt.plot(output)
    #plt.plot(real)
    plt.plot(integer)

    plt.show()

def plot_SMA(path):
    quotes = pd.read_csv(path)
    quotes.index = pd.to_datetime(quotes['date'])
    close = pd.to_datetime(quotes['4. close'])
    output = talib.SMA(close)
    plt.plot(output)
    plt.show()

if __name__ == "__main__":
    aapl_path = 'data/aapl.csv'

    #data = get_quotes('AAPL')
    #write_csv(aapl_path, data)

    #data = get_quotes('AAPL')
    #append_csv(aapl_path, data)

    plot_SMA(aapl_path)

    #plot_candlestick(aapl_path)




