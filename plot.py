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

from plotly.offline import plot
import plotly.graph_objs as go

import backtrader as bt

def plot_candlestick(file):
    quotes = pd.read_csv(file)
    quotes.index = pd.to_datetime(quotes['date'])

    _open = pd.to_datetime(quotes['1. open'])
    high = pd.to_datetime(quotes['2. high'])
    low = pd.to_datetime(quotes['3. low'])
    close = pd.to_datetime(quotes['4. close'])
    volume = pd.to_datetime(quotes['5. volume'])

    upper, middle, lower = talib.BBANDS(close, timeperiod=14)
    upper.index = upper.index.shift(periods=1, freq=-5)
    print(upper)

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
        fig, axs = plt.subplots(4, 2)
        fig.suptitle(file)
        axs[0, 0].set_title('candlestick')
        #ax = fig.add_subplot(2, 2, 1)
        candlestick_ohlc(axs[0, 0], zip(mdates.date2num(quotes.index), quotes['1. open'], quotes['2. high'],quotes['3. low'], quotes['4. close']),width=0.6,colorup='r', colordown='g')
        axs[0, 0].xaxis_date()

        axs[0, 0].plot(upper)
        axs[0, 0].plot(middle)
        axs[0, 0].plot(lower)

        axs[0, 0].autoscale_view()


    SMA_output = talib.SMA(close)
    AD_output = talib.AD(high, low, close, volume)
    BBANDS = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    axs[1, 0].set_title('SMA_output')
    axs[1, 0].plot(SMA_output, 'tab:green')
    axs[1, 0].xaxis_date()
    axs[1, 0].autoscale_view()

    axs[2, 0].set_title('AD_output')
    axs[2, 0].plot(AD_output, 'tab:orange')
    axs[2, 0].xaxis_date()
    axs[2, 0].autoscale_view()

    axs[3, 0].set_title('BBANDS')
    axs[3, 0].plot(upper)
    axs[3, 0].plot(middle)
    axs[3, 0].plot(lower)
    axs[3, 0].xaxis_date()
    axs[3, 0].autoscale_view()

    plt.show()


def plot_trace(trace):
    data = [trace]
    plot(data, filename='go_candle1.html')

