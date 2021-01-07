import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from alpha_vantage.techindicators import TechIndicators

from quote_data import *
from plot import *

# set how many past days to check
total_past_days = 1

def macd_analysis(symbol, outputsize = 'compact'):
    key = 'B478G0MJQCKU8MKM'
    at = TechIndicators(key, output_format='pandas')
    macd_data, meta_data = at.get_macd(symbol, interval='daily', series_type='close', fastperiod=12, slowperiod=26, signalperiod=9)
    #print(macd_data[:1])

    dif = macd_data['MACD']
    dea = macd_data['MACD_Signal']
    macd_hist = macd_data['MACD_Hist']

    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    # extract Final historical df
    df = pd.DataFrame(quotes)
    # extract OHLC
    close = df['4. close']

    past_days = 0
    flag = 0
    for index, row in macd_data.iterrows():
        date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')
        if past_days < total_past_days + 1:
            if dif[past_days] > 0 and dea[past_days] > 0:
                if macd_hist[past_days] > 0 and macd_hist[past_days+1] < 0:
                    print('macd bull cross 1 金叉')
                    flag = 1
                elif macd_hist[past_days] > macd_hist[past_days+1]:
                    print('macd bull 2')
                    flag = 1
                elif macd_hist[past_days] < macd_hist[past_days+1]:
                    print('macd bull caution down!!!')
                    flag = 1
                elif dif[past_days] > dif[past_days+1] and dea[past_days] > dea[past_days+1]:
                    print('macd bull 3')
                    flag = 1
                elif dif[past_days] < dif[past_days+1] and dea[past_days] < dea[past_days+1]:
                    print('macd small bear 3')
                    flag = 1
                if flag:
                    print(index)
                    print(row)
                    print('----------------------------------------\n')
            elif dif[past_days] < 0 and dea[past_days] < 0:
                if macd_hist[past_days] < 0 and macd_hist[past_days+1] > 0:
                    print('macd bear cross 1 死叉')
                    flag = 1
                elif macd_hist[past_days] < macd_hist[past_days+1]:
                    print('macd bear 2')
                    flag = 1
                elif dif[past_days] < dif[past_days+1] and dea[past_days] < dea[past_days+1]:
                    print('macd bear 3')
                    flag = 1
                elif dif[past_days] > dif[past_days+1] and dea[past_days] > dea[past_days+1]:
                    print('macd bull caution up!!!')
                    flag = 1
                elif macd_hist[past_days] > 0 and macd_hist[past_days+1] < 0:
                    print('macd bull cross caution!!!')
                    flag = 1
                if flag:
                    print(index)
                    print(row)
                    print('----------------------------------------\n')

            if close[past_days] > close[past_days+1]:
                if macd_hist[past_days] < macd_hist[past_days+1]:
                    print('macd bear caution!!! 顶背离 sell')
            elif close[past_days] < close[past_days+1]:
                if macd_hist[past_days] > macd_hist[past_days+1]:
                    print('macd bull caution!!! 底背离 caution buy')

        past_days = past_days + 1

    return
