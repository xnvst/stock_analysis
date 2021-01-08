import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from alpha_vantage.techindicators import TechIndicators

from quote_data import *
from plot import *

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
                if past_days == 0:
                    print('********' + str(index) + '************************')
                else:
                    print(index)
                    print(row)
                    print(df.loc[past_days])
                print('----------------------------------------\n')
                pass

        past_days = past_days + 1

    return


def price_volume_analysis(symbol, outputsize = 'compact'):
    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    # extract Final historical df
    df = pd.DataFrame(quotes)

    close = df['4. close']
    volume = df['5. volume']
    print(close)

#    key = 'B478G0MJQCKU8MKM'
#    at = TechIndicators(key, output_format='pandas')
#    ema_data, meta_data = at.get_ema(symbol, interval='daily', time_period=10, series_type='close')
#    print(ema_data)
#    print(ema_data.shape)
#    print(ema_data.loc[ema_data.index[1]])

    past_days = 0
    alpha = 0.3
    beta = 0.01
    while past_days < total_past_days + 1:
        date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')

        flag = 0
        close_mean = np.mean(close[:10])
        vol_mean = np.mean(volume[:10])
        if close[past_days] > close_mean * (1+beta):
            if volume[past_days] < vol_mean * (1+alpha) and volume[past_days] > vol_mean * (1-alpha):
                print('高位无量就要拿，拿错也要拿')
                flag = 1
            elif volume[past_days] > vol_mean * (1+alpha):
                print('高位放量就要跑，跑错也要跑')
                flag = 1
        elif close[past_days] < close_mean * (1-beta):
            if volume[past_days] < vol_mean * (1+alpha) and volume[past_days] > vol_mean * (1-alpha):
                print('低位无量就要等,等错也要等')
                flag = 1
            elif volume[past_days] > vol_mean * (1+alpha):
                print('低位放量就要跟,跟错也要跟')
                flag = 1

        if flag:
            if past_days == 0:
                print('********' + date + '************************')
            else:
                print(date)
                print(close[past_days])
                print(volume[past_days])
                print(close_mean)
                print(vol_mean)
            print('----------------------------------------\n')

        past_days = past_days + 1

    return


'''
高位无量就要拿，拿错也要拿
高位放量就要跑，跑错也要跑
低位无量就要等,等错也要等
低位放量就要跟,跟错也要跟

量增价升，一定进场！         量增价升，买入信号.
量增价平，高位走人！         量增价平，转阳信号.
量增价跌，走为上策！         量增价跌，弃卖观望.
量平价稳，一定盘整！

量平价升，低位不跟！         量平价升，持续买入.
量平价跌，还要下跌！         量平价跌，继续卖出.
量减价升，提高警惕！         量减价升，继续持有.
量减价平，提高警戒！         量减价平，警戒信号.

量减价跌，天天要跌！         量减价跌，卖出信号.
谷底地量，将要上涨！
天量出天价，地量出地价！
无量上涨天天涨！
无量下跌天天跌！

作者：圭途
链接：https://xueqiu.com/3899772484/77695502
来源：雪球
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
风险提示：本文所提到的观点仅代表个人的意见，所涉及标的不作推荐，据此买卖，风险自负。
'''