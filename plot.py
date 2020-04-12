from alpha_vantage.timeseries import TimeSeries

import operator

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from matplotlib.dates import DateFormatter

import mpl_finance as mpf
from mpl_finance import candlestick_ohlc

import numpy
import talib

def plot_candlestick(path):
    quotes = pd.read_csv(path)
    quotes.index = pd.to_datetime(quotes['date'])

    if False:
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

    if True:
        fig = plt.figure(figsize=(24, 8))
        ax = fig.add_subplot(1, 2, 1)
        candlestick_ohlc(ax, zip(mdates.date2num(quotes.index), quotes['1. open'], quotes['2. high'],quotes['3. low'], quotes['4. close']),width=0.6,colorup='r', colordown='g')
        ax.xaxis_date()
        ax.autoscale_view()

    _open = pd.to_datetime(quotes['1. open'])
    high = pd.to_datetime(quotes['2. high'])
    low = pd.to_datetime(quotes['3. low'])
    close = pd.to_datetime(quotes['4. close'])
    volume = pd.to_datetime(quotes['5. volume'])

    SMA_output = talib.SMA(close)
    AD_output = talib.AD(high, low, close, volume)
    CDL2CROWS_output = talib.CDL2CROWS(_open, high, low, close)

    #plt.subplot(1, 2, 2)
    plt.figure('SMA_output')
    plt.plot(SMA_output)

    #plt.subplot(1, 2, 2)
    plt.figure('AD_output')
    plt.plot(AD_output)

    plt.figure('CDL2CROWS_output')
    plt.plot(CDL2CROWS_output)

    plt.show()

