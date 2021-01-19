import sys, getopt

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

def SetColor(x):
    if(x < 0):
        return "red"
    else:
        return "green"

def SetVolumeColor(op, cl):
    if(cl < op):
        return "red"
    else:
        return "green"

def all_analysis():
    keycnt = 0
    technical_list = []
    for s in my_symbols:
        # step 1 - collect quote
        file = collect_quote(s, outputsize = 'compact', append = 1, print_debug = 0, key_cnt = keycnt)
        collect_macd_data(s, append = 1, print_debug = 0, key_cnt = keycnt)
        collect_mfi_data(s, append = 1, print_debug = 0, key_cnt = keycnt)

        # step 2 - analysis
        print('\n\n$$$----------------------------------------')
        print(s)
        candle_pattern_recognition(s)
        t1, t2, t3 = technical_analysis(s, key_cnt = keycnt)
        print("symbol, macd, price_volume, mfi: \n" + s + ', ' + str(t1) + ', ' + str(t2) + ', ' + str(t3))
        technical_list.append((s, t1, t2, t3))
        print('###----------------------------------------\n\n')

        keycnt += 1
        print('keycnt = ', str(keycnt))

    technical_list.sort(key = (lambda elem : (elem[1], elem[2], elem[3])), reverse=True)
    print("symbol, macd, price_volume, mfi\n")
    for x in range(len(technical_list)):
        print(technical_list[x])
    return

def single_analysis(s):
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

    data0 = go.Bar(
            x=df['date'],
            y=volume, #df['4. close'],
            name='volume',
            marker=dict(color=list(map(SetVolumeColor, op, cl))),
            #marker=color,
            )

    t1, t2, t3 = technical_analysis(s, key_cnt = 0)

    data1 = go.Bar(
            x=df['date'],
            y=t1, #df['4. close'],
            name='macd',
            marker=dict(color=list(map(SetColor, t1))),
            #marker=color,
            )
    data2 = go.Bar(
            x=df['date'],
            y=t2, #df['4. close'],
            name='price_volume',
            marker=dict(color=list(map(SetColor, t2))),
            #marker=color,
            )
    data3 = go.Bar(
            x=df['date'],
            y=t3, #df['4. close'],
            name='mfi',
            marker=dict(color=list(map(SetColor, t3))),
            #marker=color,
            )

    #fig = go.Figure([trace, data2])    # plot together

    fig = make_subplots(rows=6, cols=1)
    fig.add_trace(trace, row=1, col=1)
    fig.add_trace(data0, row=3, col=1)
    fig.add_trace(data1, row=4, col=1)
    fig.add_trace(data2, row=5, col=1)
    fig.add_trace(data3, row=6, col=1)

    #candle_pattern_recognition(s, enable_plot = plot)
    fig.update_layout(
        title=s,
        height=1200,
        #yaxis_title='AAPL Stock',
        #shapes = [dict(
        #    x0=s_date, x1=s_date, y0=0, y1=1, xref='x', yref='paper',
        #    line_width=2)],
        #annotations=[dict(
        #    x=s_date, y=-0.05, xref='x', yref='paper',
        #    showarrow=False, xanchor='left', text='Increase Period Begins')]
    )

    fig['layout']['yaxis1'].update(domain=[0.7, 1])
    fig['layout']['yaxis3'].update(domain=[0.3, 0.5])
    fig['layout']['yaxis4'].update(domain=[0.2, 0.29])
    fig['layout']['yaxis5'].update(domain=[0.1, 0.19])
    fig['layout']['yaxis6'].update(domain=[0, 0.09])

    fig.write_html('result/'+s+'.html')
    fig.show()
    return

'''
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
'''

def main(argv):
   symbol = ''
   try:
      opts, args = getopt.getopt(argv,"hs:")
   except getopt.GetoptError:
      print('main.py -s <symbol>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('main.py -s <symbol>')
         sys.exit()
      elif opt in ("-s"):
         symbol = arg
   print('symbol is ' + symbol)
   return symbol

if __name__ == "__main__":
    print('welcome!\n')

    symbol = main(sys.argv[1:])
    if symbol == 'all':
        all_analysis()
    else:
        single_analysis(symbol)


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
