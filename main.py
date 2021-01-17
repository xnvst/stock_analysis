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

def colorize_data(x):
    color = []
    c = ''
    for i in x:
        if i>0:
            c = 'green'
        else:
            c = 'red'
        color.append(c)
    return color


if __name__ == "__main__":
    print('welcome!\n')

    s = 'MA'
    plot = 1
    file = collect_quote(s, append = 0)
    quotes = pd.read_csv(file)
    df = pd.DataFrame(quotes)

    past_days = 5
    s_date = df.loc[df.index[past_days]]['date']

    op = df['1. open']
    hi = df['2. high']
    lo = df['3. low']
    cl = df['4. close']
    volume = df['5. volume']
    trace = go.Candlestick(
                x = df['date'],
                open=op,
                high=hi,
                low=lo,
                close=cl)

    t1, t2, t3 = technical_analysis(s, key_cnt = 0)
    print(t1)

    #color=colorize_data(t1)
    data1 = go.Bar(
            x=df['date'],
            y=t1, #df['4. close'],
            name='macd',
            marker=dict(color='green'),
            #marker=color,
            )
    data2 = go.Bar(
            x=df['price_volume'],
            y=t2, #df['4. close'],
            name='test',
            marker=dict(color='green'),
            #marker=color,
            )
    data3 = go.Bar(
            x=df['date'],
            y=t3, #df['4. close'],
            name='mfi',
            marker=dict(color='green'),
            #marker=color,
            )

    #fig = go.Figure([trace, data2])    # plot together

    fig = make_subplots(rows=4, cols=1)
    fig.add_trace(trace, row=1, col=1)
    fig.add_trace(data1, row=2, col=1)
    fig.add_trace(data2, row=3, col=1)
    fig.add_trace(data3, row=4, col=1)

    #candle_pattern_recognition(s, enable_plot = plot)
    fig.update_layout(
        title='The Great Recession',
        yaxis_title='AAPL Stock',
        shapes = [dict(
            x0=s_date, x1=s_date, y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x=s_date, y=-0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='Increase Period Begins')]
    )

    fig.show()

    sys.exit(0)

    t1, t2, t3 = technical_analysis(s, key_cnt = 0)
    print(t1)

    fig.show()
    sys.exit(0)

    fig.update_layout(
        title='The Great Recession',
        yaxis_title='AAPL Stock',
        shapes = [dict(
            x0='2020-12-09', x1='2020-12-09', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x='2020-12-09', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='Increase Period Begins')]
    )

    fig.show()
    sys.exit(0)
    ##################################################

    keycnt = 0
    technical_list = []
    for s in my_symbols_now:
        # step 1 - collect quote
        file = collect_quote(s, outputsize = 'compact', append = 1, print_debug = 0, key_cnt = keycnt)

        # step 2 - analysis
        print('\n\n$$$----------------------------------------')
        print(s)
        candle_pattern_recognition(s)
        t1, t2, t3 = technical_analysis(s, key_cnt = keycnt)
        print("symbol, macd, price_volume, mfi: \n" + s + ', ' + str(t1) + ', ' + str(t2) + ', ' + str(t3))
        technical_list.append((s, t1, t2, t3))
        print('###----------------------------------------\n\n')

        keycnt += 1


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
