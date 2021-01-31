import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from alpha_vantage.techindicators import TechIndicators

from quote_data import *
from plot import *

def technical_analysis(symbol, en_macd = 1, en_pv = 1, en_mfi = 0):
    t1 = []
    t2 = []
    t3 = []
    dfi = []
    dea = []
    mfi = []
    macd_hist = []
    macd_str = ''
    t2_str = ''
    t3_str = ''
    if en_macd:
        t1, dfi, dea, macd_hist, macd_str = macd_analysis(symbol)
    if en_pv:
        t2, t2_str = price_volume_analysis(symbol)
    if en_mfi:
        t3, mfi, t3_str = mfi_analysis(symbol)
    K, D, J = kdj_analysis(symbol)
    return t1, dfi, dea, macd_hist, t2, t3, mfi, macd_str, t2_str, t3_str, K, D, J

def collect_macd_data(symbol, append = 0, print_debug = 0, key_cnt = 0, fastperiod=6, slowperiod=13, signalperiod=5):
    symbol_file = 'data/' + symbol + '_macd.csv'

    if Path(symbol_file).is_file():
        if append == 1:
            at = TechIndicators(key, output_format='pandas')
            try:
                data, meta_data = at.get_macd(symbol, interval='daily', series_type='close', fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
            except:
                print("macd_analysis exception")
            api_delay(key_cnt)
            if print_debug == 1:
                print (symbol_file + " exist & append")
            append_csv(symbol_file, data)
        else:
            if print_debug == 1:
                print (symbol_file + " exist")
            pass
    else:
        at = TechIndicators(key, output_format='pandas')
        try:
            data, meta_data = at.get_macd(symbol, interval='daily', series_type='close', fastperiod=12, slowperiod=26, signalperiod=9)
        except:
            print("macd_analysis exception")
        api_delay(key_cnt)
        print (symbol_file + " created")
        write_csv(symbol_file, data)
    return symbol_file

def collect_mfi_data(symbol, append = 0, print_debug = 0, key_cnt = 0):
    symbol_file = 'data/' + symbol + '_mfi.csv'

    if Path(symbol_file).is_file():
        if append == 1:
            at = TechIndicators(key, output_format='pandas')
            try:
                data, meta_data = at.get_mfi(symbol, interval='daily', time_period=14, series_type='close')
            except:
                print("mfi_analysis exception")
            api_delay(key_cnt)
            if print_debug == 1:
                print (symbol_file + " exist & append")
            append_csv(symbol_file, data)
        else:
            if print_debug == 1:
                print (symbol_file + " exist")
            pass
    else:
        at = TechIndicators(key, output_format='pandas')
        try:
            data, meta_data = at.get_mfi(symbol, interval='daily', time_period=14, series_type='close')
        except:
            print("mfi_analysis exception")
        api_delay(key_cnt)
        print (symbol_file + " created")
        write_csv(symbol_file, data)
    return symbol_file

def kdj_analysis(symbol):
    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    df = pd.DataFrame(quotes)

    op = df['1. open']
    hi = df['2. high']
    lo = df['3. low']
    close = df['4. close']
    volume = df['5. volume']

    low_list = lo.rolling(9, min_periods=9).min()
    low_list.fillna(value = lo.expanding().min(), inplace = True)
    high_list = hi.rolling(9, min_periods=9).max()
    high_list.fillna(value = hi.expanding().max(), inplace = True)
    rsv = (close - low_list) / (high_list - low_list) * 100

    df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    return df['K'], df['D'], df['J']

def macd_analysis(symbol):
    tenhnical_cnt_list = []
    macd_str = []

    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    # extract Final historical df
    df = pd.DataFrame(quotes)

    file = collect_macd_data(symbol, append = 0)
    quotes = pd.read_csv(file)
    df_macd = pd.DataFrame(quotes)

    dfi = df_macd['MACD']
    dea = df_macd['MACD_Signal']
    macd_hist = df_macd['MACD_Hist']

    past_days = 0
    for index, row in df_macd.iterrows():
        #date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')
        if past_days < total_past_days + 1:
            tenhnical_cnt = 0
            w_str = ''

            flag1 = 0
            if dfi[past_days] > 0 and dea[past_days] > 0:
                if macd_hist[past_days] > 0 and macd_hist[past_days+1] < 0:
                    w = 'macd bull 1.1: 金叉'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt += 2
                    flag1 = 1
                elif dfi[past_days] > dfi[past_days+1] and dea[past_days] > dea[past_days+1]:
                    w = 'macd bull 1.2: 多头行情中,可以买入或持股'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt += 0.5
                    flag1 = 1
                elif dfi[past_days] < dfi[past_days+1] and dea[past_days] < dea[past_days+1]:
                    w = 'macd bear 1.3: 退潮阶段,股票将下跌,可以卖出股票和观望'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt -= 1
                    flag1 = 1
            elif dfi[past_days] < 0 and dea[past_days] < 0:
                if macd_hist[past_days] < 0 and macd_hist[past_days+1] > 0:
                    w = 'macd bear 1.1: 死叉'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt -= 2
                    flag1 = 1
                elif macd_hist[past_days] > 0 and macd_hist[past_days+1] < 0:
                    w = 'macd bull 1.3: 金叉2'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt += 1.5
                    flag1 = 1
                elif dfi[past_days] < dfi[past_days+1] and dea[past_days] < dea[past_days+1]:
                    w = 'macd bear 1.2: 空头行情中,可以卖出股票或观望'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt -= 0.5
                    flag1 = 1
                elif dfi[past_days] > dfi[past_days+1] and dea[past_days] > dea[past_days+1]:
                    w = 'macd bull 1.4: 行情即将启动,股票将上涨,可以买进股票或持股待涨'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt += 1
                    flag1 = 1

            flag2 = 0
            if macd_hist[past_days] > 0 and macd_hist[past_days+1] > 0:
                if macd_hist[past_days] < macd_hist[past_days+1]:
                    w = 'macd bear 2.1: 绿柱状缩小,进入调整期'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt -= 0.5
                    flag2 = 1
                elif macd_hist[past_days] > macd_hist[past_days+1]:
                    w = 'macd bull 2.1: 当绿柱状持续放大时,表明股市处于牛市行情中,股价将继续上涨'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt += 1
                    flag2 = 1
            elif macd_hist[past_days] < 0 and macd_hist[past_days+1] < 0:
                if macd_hist[past_days] < macd_hist[past_days+1]:
                    w = 'macd bear 2.2: 当红柱状持续放大时,表明股市处于熊市行情之中,股价将继续下跌'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt -= 1
                    flag2 = 1
                elif macd_hist[past_days] > macd_hist[past_days+1]:
                    w = 'macd bull 2.2: 当红柱状开始收缩时,表明股市的大跌行情即将结束,股价将止跌向上或进入盘整'
                    print(w)
                    w_str += str(w + ';\n')
                    tenhnical_cnt -= 0.5
                    flag2 = 1

            flag3 = 0
            close = df['4. close']
            bottom_diverge = 1
            top_diverge = 1
            for i in range(3):
                if close[past_days+i] < close[past_days+i+1] and macd_hist[past_days+i] > macd_hist[past_days+i+1]:
                    continue
                else:
                    bottom_diverge = 0
                    pass
                if close[past_days+i] > close[past_days+i+1] and macd_hist[past_days+i] < macd_hist[past_days+i+1]:
                    continue
                else:
                    top_diverge = 0
                    pass
            if bottom_diverge:
                w = 'macd bull caution!!! 底背离 buy'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt += 2
                flag3 = 1
            if  top_diverge:
                w = 'macd bear caution!!! 顶背离 sell'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 2
                flag3 = 1

            if flag1 or flag2 or flag3:
                if past_days == 0:
                    print('********' + df.loc[df.index[past_days]]['date'] + '************************')
                    print(row)
                    print(df.loc[past_days])
                    print('macd tenhnical_cnt: ' + str(tenhnical_cnt))
                else:
                    print(df.loc[df.index[past_days]]['date'])
                    print('macd tenhnical_cnt: ' + str(tenhnical_cnt))
                print('----------------------------------------\n')
                macd_str.append(w_str)
                pass

            tenhnical_cnt_list.append(tenhnical_cnt)
        past_days = past_days + 1

    if not macd_str:
        macd_str = ['']

    return tenhnical_cnt_list, dfi, dea, macd_hist, macd_str[0]


def price_volume_analysis(symbol):
    tenhnical_cnt_list = []
    data_str = []

    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    # extract Final historical df
    df = pd.DataFrame(quotes)

    op = df['1. open']
    hi = df['2. high']
    lo = df['3. low']
    close = df['4. close']
    volume = df['5. volume']

#    key = 'B478G0MJQCKU8MKM'
#    at = TechIndicators(key, output_format='pandas')
#    ema_data, meta_data = at.get_ema(symbol, interval='daily', time_period=10, series_type='close')
#    print(ema_data)
#    print(ema_data.shape)
#    print(ema_data.loc[ema_data.index[1]])
#    api_delay(key_cnt)

    short_period = 5
    long_period = 20

    volume_alpha = 0.2
    price_alpha = 0.02

    short_close_mean = np.mean(close[:short_period])
    short_vol_mean = np.mean(volume[:short_period])

    long_close_mean = np.mean(close[:long_period])
    long_vol_mean = np.mean(volume[:long_period])

    past_days = 0
    while past_days < total_past_days + 1:
        #date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')
        tenhnical_cnt = 0
        flag = 0
        w_str = ''

        price_up = close[past_days] > short_close_mean * (1+price_alpha) and close[past_days] > long_close_mean * (1+price_alpha)
        price_similar = short_close_mean < long_close_mean * (1+volume_alpha) and short_close_mean > long_close_mean * (1-volume_alpha)
        price_down = close[past_days] < short_close_mean * (1-price_alpha) and close[past_days] < long_close_mean * (1-price_alpha)

        high_position = short_close_mean > long_close_mean    #高位
        low_position = short_close_mean < long_close_mean    #低位

        vol_up = volume[past_days] > short_vol_mean * (1+volume_alpha) and volume[past_days] > long_vol_mean * (1+volume_alpha)
        vol_similar = short_vol_mean < long_vol_mean * (1+volume_alpha) and short_vol_mean > long_vol_mean * (1-volume_alpha)
        vol_down = volume[past_days] < short_vol_mean * (1-volume_alpha) and volume[past_days] < long_vol_mean * (1-volume_alpha)

        if vol_up:
            if price_up:
                w = '量增价升，一定进场'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt += 2
                flag = 1
            elif price_similar:
                w = '量增价平，高位走人'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 0.5
                flag = 1
            elif price_down:
                w = '量增价跌，走为上策'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 2
                flag = 1
        elif vol_down:
            if price_up:
                w = '量减价升，提高警惕'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 0.5
                flag = 1
            elif price_similar:
                w = '量减价平，提高警戒'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 0.5
                flag = 1
            elif price_down:
                w = '量减价跌，天天要跌'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 2
                flag = 1

        if high_position:
            if vol_up:
                w = '高位放量就要跑，跑错也要跑'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt -= 1
                flag = 1
            else:
                w = '高位无量就要拿，拿错也要拿'
                print(w)
                w_str += str(w + ';\n')
                flag = 1
        elif low_position:
            if vol_up:
                w = '低位放量就要跟,跟错也要跟'
                print(w)
                w_str += str(w + ';\n')
                tenhnical_cnt += 1
                flag = 1
            else:
                w = '低位无量就要等,等错也要等'
                print(w)
                w_str += str(w + ';\n')
                flag = 1

        if flag:
            if past_days == 0:
                print('********' + df.loc[df.index[past_days]]['date'] + '************************')
                print(df.loc[df.index[past_days]])
                print('price_volume_analysis tenhnical_cnt: ' + str(tenhnical_cnt))
            else:
                print(df.loc[df.index[past_days]])
                print('price_volume_analysis tenhnical_cnt: ' + str(tenhnical_cnt))
            print('----------------------------------------\n')
            data_str.append(w_str)

        tenhnical_cnt_list.append(tenhnical_cnt)
        past_days = past_days + 1

    if 0:
        typical_price = (hi + lo + close)/3.0
        raw_money_flow = typical_price * volume
        past_days = 0
        while past_days < total_past_days + 1:
            print('----------------------------------------\n')
            print(df.loc[df.index[past_days]]['date'])
            print(raw_money_flow[past_days])
            print('----------------------------------------\n')
            past_days = past_days + 1

    if not data_str:
        data_str = ['']

    return tenhnical_cnt_list, data_str[0]


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

'''
《懒人炒股心经》

早盘大跌可加仓
早盘大涨要减仓
下午大涨只减仓
下午大跌次日买
'''

def mfi_analysis(symbol):
    tenhnical_cnt_list = []
    data_str = []

    file = collect_quote(symbol, append = 0)
    quotes = pd.read_csv(file)
    # extract Final historical df
    df = pd.DataFrame(quotes)
    close = df['4. close']

    sma_200 = []
    for i in range(180):
        x = np.mean(close[i:200-1+i])
        sma_200.append(x)

    try:
        file = collect_mfi_data(symbol, append = 0)
    except:
        print("collect_mfi_data exception")
        return

    quotes = pd.read_csv(file)
    df_mfi = pd.DataFrame(quotes)

    mfi = []
    for index, row in df_mfi.iterrows():
        mfi.append(df_mfi.loc[df_mfi.index[index]]['MFI'])
    #print(mfi)

    short_period = 5
    long_period = 20

    price_alpha = 0.02

    short_mfi_mean = np.mean(mfi[:short_period])
    long_mfi_mean = np.mean(mfi[:long_period])
    #print(short_mfi_mean)

    high_position = short_mfi_mean > 80    #高位
    low_position = short_mfi_mean < 20    #低位

    # mfi is in reverse order of date
    past_days = 0
    while past_days < total_past_days + 1:
        tenhnical_cnt = 0
        flag = 0
        w_str = ''

#if prive > 200MA ignore sell
#if price < 200MA ignore buy
        ignore_sell = 0
        ignore_buy = 0
        if close[past_days] > sma_200[past_days]:
            ignore_sell = 1
        else:
            ignore_buy = 1

        if mfi[past_days] > 80 and not(ignore_sell):
            w = ('MFI 超买')
            print(w)
            w_str += str(w + ';\n')
            tenhnical_cnt -= 0.5
            flag = 1
        elif mfi[past_days] < 20 and not(ignore_buy):
            w = ('MFI 超卖')
            print(w)
            w_str += str(w + ';\n')
            tenhnical_cnt += 0.5
            flag = 1

        if (mfi[past_days+1] > 80 or high_position) and mfi[past_days] < 80 and not(ignore_sell):
            w = ('MFI short trade')
            print(w)
            w_str += str(w + ';\n')
            tenhnical_cnt -= 1
            flag = 1
        elif (mfi[past_days+1] < 20 or low_position) and mfi[past_days] > 20 and not(ignore_buy):
            w = ('MFI long trade')
            print(w)
            w_str += str(w + ';\n')
            tenhnical_cnt += 1
            flag = 1

        #TODO: check price & mfi divergence: price up, mfi ~80 and down; price down, mfi ~20 and up

        if flag:
            if past_days == 0:
                print('********' + df_mfi.loc[df_mfi.index[past_days]]['date'] + '************************')
                print('mfi tenhnical_cnt: ' + str(tenhnical_cnt))
            else:
                print(df_mfi.loc[df_mfi.index[past_days]]['date'])
                print('mfi tenhnical_cnt: ' + str(tenhnical_cnt))
            print('----------------------------------------\n')
            data_str.append(w_str)

        tenhnical_cnt_list.append(tenhnical_cnt)
        past_days = past_days + 1

    if not data_str:
        data_str = ['']

    return tenhnical_cnt_list, mfi, data_str[0]
