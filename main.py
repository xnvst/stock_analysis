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

def all_collect_quotes():
    keycnt = 0
    for s in my_symbols:
        # step 1 - collect quote
        print(s)
        file = collect_quote(s, outputsize = 'compact', append = 1, print_debug = 0, key_cnt = keycnt)
        collect_macd_data(s, append = 1, print_debug = 0, key_cnt = keycnt)
        collect_mfi_data(s, append = 1, print_debug = 0, key_cnt = keycnt)
        keycnt += 1
        print('keycnt = ', str(keycnt))
    return

def all_symbol_analysis():
    technical_list = []
    for s in my_symbols:
        print('\n\n$$$----------------------------------------')
        print(s)
        candle_pattern_recognition(s)
        t1, dfi, dea, t2, t3, mfi = technical_analysis(s)
        print("symbol, macd, price_volume, mfi: \n" + s + ', ' + str(t1) + ', ' + str(t2) + ', ' + str(t3))
        technical_list.append((s, t1, t2, t3))
        print('###----------------------------------------\n\n')
    technical_list.sort(key = (lambda elem : (elem[1], elem[2], elem[3])), reverse=True)
    print("symbol, macd, price_volume, mfi\n")
    for x in range(len(technical_list)):
        print(technical_list[x])
    return

def active_symbol_analysis():
    for s in my_symbols_now:
        single_analysis(s)
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

    sma_10 = []
    sma_20 = []
    sma_50 = []
    for i in range(180):
        x = np.mean(cl[i:10-1+i])
        sma_10.append(x)
        x = np.mean(cl[i:20-1+i])
        sma_20.append(x)
        x = np.mean(cl[i:50-1+i])
        sma_50.append(x)
    data_sma_10 = go.Scatter(
            x=df['date'],
            y=sma_10,
            name='sma_10',
            marker=dict(color='orange'),
            )
    data_sma_20 = go.Scatter(
            x=df['date'],
            y=sma_20,
            name='sma_20',
            marker=dict(color='purple'),
            )
    data_sma_50 = go.Scatter(
            x=df['date'],
            y=sma_50,
            name='sma_50',
            marker=dict(color='grey'),
            )

    data0 = go.Bar(
            x=df['date'],
            y=volume,
            name='volume',
            marker=dict(color=list(map(SetVolumeColor, op, cl))),
            )

    candle_pattern_recognition(s)
    t1, dfi, dea, t2, t3, mfi = technical_analysis(s)

    data1 = go.Bar(
            x=df['date'],
            y=t1,
            name='macd score',
            marker=dict(color=list(map(SetColor, t1))),
            )
    data_dfi = go.Scatter(
            x=df['date'],
            y=dfi,
            name='dfi',
            marker=dict(color='green'),
            )
    data_dea = go.Scatter(
            x=df['date'],
            y=dea,
            name='dea',
            marker=dict(color='red'),
            )

    data2 = go.Bar(
            x=df['date'],
            y=t2,
            name='price_volume score',
            marker=dict(color=list(map(SetColor, t2))),
            )

    data3 = go.Bar(
            x=df['date'],
            y=np.multiply(t3, 10),
            name='mfi score',
            marker=dict(color=list(map(SetColor, t3))),
            )
    data_mfi = go.Scatter(
            x=df['date'],
            y=mfi,
            name='mfi',
            marker=dict(color=list(map(SetColor, t3))),
            )

    #fig = go.Figure([trace, data2])    # plot together

    fig = make_subplots(rows=8, cols=1)
    fig.add_trace(trace, row=1, col=1)
    fig.add_trace(data_sma_10, row=1, col=1)
    fig.add_trace(data_sma_20, row=1, col=1)
    fig.add_trace(data_sma_50, row=1, col=1)
    fig.add_trace(data0, row=3, col=1)

    fig.add_trace(data_dfi, row=4, col=1)
    fig.add_trace(data_dea, row=4, col=1)
    fig.add_trace(data1, row=5, col=1)

    fig.add_trace(data2, row=6, col=1)

    fig.add_trace(data_mfi, row=7, col=1)
    fig.add_trace(data3, row=8, col=1)

    #candle_pattern_recognition(s, enable_plot = plot)
    fig.update_layout(
        title=s,
        height=1200,
        xaxis_rangeslider_visible=False,
        #yaxis_title='AAPL Stock',
        #shapes = [dict(
        #    x0=s_date, x1=s_date, y0=0, y1=1, xref='x', yref='paper',
        #    line_width=2)],
        #annotations=[dict(
        #    x=s_date, y=-0.05, xref='x', yref='paper',
        #    showarrow=False, xanchor='left', text='Increase Period Begins')]
    )

    h1 = 0.15
    h2 = 0.05
    h_space = 0.01
    fig['layout']['yaxis1'].update(domain=[6*h_space+3*h2+3*h1, 1])
    fig['layout']['yaxis3'].update(domain=[5*h_space+3*h2+2*h1, 5*h_space+3*h2+3*h1])
    fig['layout']['yaxis4'].update(domain=[4*h_space+3*h2+h1, 4*h_space+3*h2+2*h1])
    fig['layout']['yaxis5'].update(domain=[3*h_space+2*h2+h1, 3*h_space+3*h2+h1])
    fig['layout']['yaxis6'].update(domain=[2*h_space+h2+h1, 2*h_space+2*h2+h1])
    fig['layout']['yaxis7'].update(domain=[h_space+h2, h_space+h2+h1])
    fig['layout']['yaxis8'].update(domain=[0, h2])

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
    if symbol == 'quote':
        all_collect_quotes()
    elif symbol == 'all':
        all_symbol_analysis()
    elif symbol == 'now':
        active_symbol_analysis()
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
