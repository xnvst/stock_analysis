import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from alpha_vantage.techindicators import TechIndicators

from quote_data import *
from plot import *

# set how many past days to check
total_past_days = 4

def macd_analysis(symbol, outputsize = 'compact'):
    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    # extract Final historical df
    df = pd.DataFrame(quotes)

    key = 'B478G0MJQCKU8MKM'
    at = TechIndicators(key, output_format='pandas')
    macd_data, meta_data = at.get_macd(symbol, interval='daily', series_type='close', fastperiod=12, slowperiod=26, signalperiod=9)
    #print(macd_data[:1])

    dif = macd_data['MACD']
    dea = macd_data['MACD_Signal']
    macd_hist = macd_data['MACD_Hist']

    past_days = 0
    for index, row in macd_data.iterrows():
        date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')
        if past_days < total_past_days + 1:

            flag1 = 0
            if dif[past_days] > 0 and dea[past_days] > 0:
                if macd_hist[past_days] > 0 and macd_hist[past_days+1] < 0:
                    print('macd bull 1.1: 金叉')
                    flag1 = 1
                elif dif[past_days] > dif[past_days+1] and dea[past_days] > dea[past_days+1]:
                    print('macd bull 1.2: 多头行情中,可以买入或持股')
                    flag1 = 1
                elif dif[past_days] < dif[past_days+1] and dea[past_days] < dea[past_days+1]:
                    print('macd bear 1.3: 退潮阶段,股票将下跌,可以卖出股票和观望')
                    flag1 = 1
            elif dif[past_days] < 0 and dea[past_days] < 0:
                if macd_hist[past_days] < 0 and macd_hist[past_days+1] > 0:
                    print('macd bear 1.1: 死叉')
                    flag1 = 1
                elif macd_hist[past_days] > 0 and macd_hist[past_days+1] < 0:
                    print('macd bull 1.3: 金叉2')
                    flag1 = 1
                elif dif[past_days] < dif[past_days+1] and dea[past_days] < dea[past_days+1]:
                    print('macd bear 1.2: 空头行情中,可以卖出股票或观望')
                    flag1 = 1
                elif dif[past_days] > dif[past_days+1] and dea[past_days] > dea[past_days+1]:
                    print('macd bull 1.4: 行情即将启动,股票将上涨,可以买进股票或持股待涨')
                    flag1 = 1

            flag2 = 0
            if macd_hist[past_days] > 0 and macd_hist[past_days+1] > 0:
                if macd_hist[past_days] < macd_hist[past_days+1]:
                    print('macd bear 2.1: 红柱状缩小,进入调整期')
                    flag2 = 1
                elif macd_hist[past_days] > macd_hist[past_days+1]:
                    print('macd bull 2.1: 当红柱状持续放大时,表明股市处于牛市行情中,股价将继续上涨')
                    flag2 = 1
            elif macd_hist[past_days] < 0 and macd_hist[past_days+1] < 0:
                if macd_hist[past_days] < macd_hist[past_days+1]:
                    print('macd bear 2.2: 当绿柱状持续放大时,表明股市处于熊市行情之中,股价将继续下跌')
                    flag2 = 1
                elif macd_hist[past_days] > macd_hist[past_days+1]:
                    print('macd bull 2.2: 当绿柱状开始收缩时,表明股市的大跌行情即将结束,股价将止跌向上或进入盘整')
                    flag2 = 1

            flag3 = 0
            close = df['4. close']
            if close[past_days] > close[past_days+1]:
                if macd_hist[past_days] < macd_hist[past_days+1]:
                    print('macd bear caution!!! 顶背离 sell')
                    flag3 = 1
            elif close[past_days] < close[past_days+1]:
                if macd_hist[past_days] > macd_hist[past_days+1]:
                    print('macd bull caution!!! 底背离 buy')
                    flag3 = 1

            if flag1 or flag2 or flag3:
                print(index)
                print(row)
                print(df.loc[past_days])
                print('----------------------------------------\n')
                pass

        past_days = past_days + 1

    return
