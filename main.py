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
        #if s != 'BMO' and keycnt == 0:
        #    continue
        #else:
        #    pass
        collect_quote(s, outputsize = 'compact', append = 1, print_debug = 0, key_cnt = keycnt)
        collect_macd_data(s, append = 1, print_debug = 0, key_cnt = keycnt)
        if 0:   # mfi not having much information, disable to save time
            collect_mfi_data(s, append = 1, print_debug = 0, key_cnt = keycnt)
        keycnt += 1
        print('keycnt = ', str(keycnt))
    return

def all_symbol_analysis():
    technical_list = []
    for s in my_symbols:
        print('\n\n$$$----------------------------------------')
        t1, dfi, dea, macd_hist, t2, t3, mfi, macd_str, t2_str, t3_str, candle_score = single_analysis(s, en_plot = 0)
        print("symbol, macd, price_volume, mfi: \n" + s + ', ' + str(t1) + ', ' + str(t2) + ', ' + str(t3)+ ', ' + str(candle_score))
        technical_list.append((s, t1, t2, t3, candle_score))
        print('###----------------------------------------\n\n')
    #technical_list.sort(key = (lambda elem : (elem[1][0] + elem[2][0] + elem[3][0] + elem[4])), reverse=True)
    technical_list.sort(key = (lambda elem : (elem[1][0] + elem[2][0] + elem[4])), reverse=True)
    print("symbol, macd, price_volume, mfi\n")
    for x in range(len(technical_list)):
        print(technical_list[x])
    return

def single_analysis(s, en_plot = 1):
    print(s)
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
    sma_200 = []
    for i in range(180):
        x = np.mean(cl[i:10-1+i])
        sma_10.append(x)
        x = np.mean(cl[i:20-1+i])
        sma_20.append(x)
        x = np.mean(cl[i:50-1+i])
        sma_50.append(x)
        x = np.mean(cl[i:200-1+i])
        sma_200.append(x)
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
            marker=dict(color='blue'),
            )
    data_sma_200 = go.Scatter(
            x=df['date'],
            y=sma_200,
            name='sma_200',
            marker=dict(color='grey'),
            )

    data0 = go.Bar(
            x=df['date'],
            y=volume,
            name='volume',
            marker=dict(color=list(map(SetVolumeColor, op, cl))),
            )

    candle_str, candle_score = candle_pattern_recognition(s)
    t1, dfi, dea, macd_hist, t2, t3, mfi, macd_str, t2_str, t3_str, K, D, J = technical_analysis(s)

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
    data_macd_hist = go.Bar(
            x=df['date'],
            y=macd_hist,
            name='macd_hist',
            marker=dict(color=list(map(SetColor, macd_hist))),
            )

    data2 = go.Bar(
            x=df['date'],
            y=t2,
            name='price_volume score',
            marker=dict(color=list(map(SetColor, t2))),
            )

    data3 = go.Bar(
            x=df['date'],
            y=t3,
            name='mfi score',
            marker=dict(color=list(map(SetColor, t3))),
            )
    data_mfi = go.Scatter(
            x=df['date'],
            y=mfi,
            name='mfi',
            marker=dict(color='black'),
            )

    mfi_20 = []
    mfi_50 = []
    mfi_80 = []
    for i in range(180):
        mfi_20.append(20)
        mfi_80.append(80)
        mfi_50.append(50)
    data_mfi_20 = go.Scatter(
            x=df['date'],
            y=mfi_20,
            #name='20',
            marker=dict(color='green'),
            )
    data_mfi_50 = go.Scatter(
            x=df['date'],
            y=mfi_50,
            #name='mfi',
            marker=dict(color='grey'),
            )
    data_mfi_80 = go.Scatter(
            x=df['date'],
            y=mfi_80,
            #name='mfi',
            marker=dict(color='red'),
            )

    data_K = go.Scatter(
            x=df['date'],
            y=K,
            name='K',
            marker=dict(color='orange'),
            )
    data_D = go.Scatter(
            x=df['date'],
            y=D,
            name='D',
            marker=dict(color='blue'),
            )
    data_J = go.Scatter(
            x=df['date'],
            y=J,
            name='J',
            marker=dict(color='purple'),
            )

    #fig = go.Figure([trace, data2])    # plot together

    fig = make_subplots(rows=8, cols=1)
    fig.add_trace(trace, row=1, col=1)
    fig.add_trace(data_sma_10, row=1, col=1)
    fig.add_trace(data_sma_20, row=1, col=1)
    fig.add_trace(data_sma_50, row=1, col=1)
    fig.add_trace(data_sma_200, row=1, col=1)
    fig.add_trace(data0, row=3, col=1)

    fig.add_trace(data_dfi, row=4, col=1)
    fig.add_trace(data_dea, row=4, col=1)
    fig.add_trace(data_macd_hist, row=4, col=1)

    fig.add_trace(data_K, row=5, col=1)
    fig.add_trace(data_D, row=5, col=1)
    fig.add_trace(data_J, row=5, col=1)
    fig.add_trace(data_mfi_20, row=5, col=1)
    fig.add_trace(data_mfi_50, row=5, col=1)
    fig.add_trace(data_mfi_80, row=5, col=1)

    fig.add_trace(data2, row=6, col=1)

    fig.add_trace(data_mfi, row=7, col=1)
    fig.add_trace(data_mfi_20, row=7, col=1)
    fig.add_trace(data_mfi_80, row=7, col=1)
    fig.add_trace(data3, row=8, col=1)

    fig.add_trace(data1, row=8, col=1)

    text_str = 'macd: ' + macd_str+' \nprice_volume: '+t2_str+' \nmfi: '+t3_str+' \ncandle: '+candle_str
    fig.update_layout(
        title=s,
        height=1200,
        xaxis_rangeslider_visible=False,
        #yaxis_title='AAPL Stock',
        #shapes = [dict(
        #    x0=s_date, x1=s_date, y0=0, y1=1, xref='x', yref='paper',
        #    line_width=2)],
        annotations=[dict(
            x=0, y=-0.05, xref='paper', yref='paper',
            showarrow=False, xanchor='left', text=text_str)]
    )

    h1 = 0.12
    h2 = 0.1
    h_space = 0.01
    fig['layout']['yaxis1'].update(domain=[6*h_space+3*h2+3*h1, 1])
    fig['layout']['yaxis3'].update(domain=[5*h_space+3*h2+2*h1, 5*h_space+3*h2+3*h1])
    fig['layout']['yaxis4'].update(domain=[4*h_space+3*h2+h1, 4*h_space+3*h2+2*h1])
    fig['layout']['yaxis5'].update(domain=[3*h_space+2*h2+h1, 3*h_space+3*h2+h1])
    fig['layout']['yaxis6'].update(domain=[2*h_space+h2+h1, 2*h_space+2*h2+h1])
    fig['layout']['yaxis7'].update(domain=[h_space+h2, h_space+h2+h1])
    fig['layout']['yaxis8'].update(domain=[0, h2])

    if en_plot:
        fig.show()
    fig.write_html('result/'+s+'.html')
    return t1, dfi, dea, macd_hist, t2, t3, mfi, macd_str, t2_str, t3_str, candle_score

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
   quote = 0
   try:
      opts, args = getopt.getopt(argv,"hq:s:")
   except getopt.GetoptError:
      print('main.py -s <symbol>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('main.py -s <symbol>')
         sys.exit()
      elif opt in ("-s"):
         symbol = arg
      elif opt in ("-q"):
         symbol = arg
         quote = 1
   print('symbol is ' + symbol)
   return symbol, quote

if __name__ == "__main__":
    print('welcome!\n')

    symbol, quote = main(sys.argv[1:])
    if symbol == 'quote':
        all_collect_quotes()
    elif symbol == 'all':
        all_symbol_analysis()
    elif symbol == 'now':
        active_symbol_analysis()
    else:
        if quote == 1:
            collect_quote(symbol, outputsize = 'compact', append = 1, print_debug = 0, key_cnt = 0)
            collect_macd_data(symbol, append = 1, print_debug = 0, key_cnt = 0)
            collect_mfi_data(symbol, append = 1, print_debug = 0, key_cnt = 0)
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
