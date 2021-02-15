import pandas as pd
import numpy as np
import talib
from itertools import compress
from datetime import datetime, timedelta

from quote_data import *
from candle_rankings import *
from plot import *

def candle_pattern_list():
    candle_names = talib.get_function_groups()['Pattern Recognition']
    for e in candle_names:
        print('"' + e + '",')
    print(candle_rankings)

def candle_pattern_recognition(s, enable_plot = 0):
    file = collect_quote(s, append = 0)
    w_str = ''
    score = 0

    quotes = pd.read_csv(file)

    # extract Final historical df
    df = pd.DataFrame(quotes)

    # extract OHLC
    op = df['1. open']
    hi = df['2. high']
    lo = df['3. low']
    cl = df['4. close']
    volume = df['5. volume']

    # candle_names = talib.get_function_groups()['Pattern Recognition']
    # create columns for each pattern
    for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        df[candle] = getattr(talib, candle)(op, hi, lo, cl)

    #print(df)

    df['candlestick_pattern'] = np.nan
    df['candlestick_match_count'] = np.nan
    for index, row in df.iterrows():
        # no pattern found
        if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
            df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
            df.loc[index, 'candlestick_match_count'] = 0
        # single pattern found
        elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
            # bull pattern 100 or 200
            if any(row[candle_names].values > 0):
                pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bull'
                df.loc[index, 'candlestick_pattern'] = pattern
                df.loc[index, 'candlestick_match_count'] = 1
            # bear pattern -100 or -200
            else:
                pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bear'
                df.loc[index, 'candlestick_pattern'] = pattern
                df.loc[index, 'candlestick_match_count'] = 1
        # multiple patterns matched -- select best performance
        else:
            # filter out pattern names from bool list of values
            patterns = list(compress(row[candle_names].keys(), row[candle_names].values != 0))
            container = []
            for pattern in patterns:
                if row[pattern] > 0:
                    container.append(pattern + '_Bull')
                else:
                    container.append(pattern + '_Bear')
            rank_list = [candle_rankings[p] for p in container]
            if len(rank_list) == len(container):
                rank_index_best = rank_list.index(min(rank_list))
                df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
                df.loc[index, 'candlestick_match_count'] = len(container)
    # clean up candle columns
    df.drop(candle_names, axis = 1, inplace = True)

    past_days = 0
    while past_days < total_past_days + 1:
        date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')
        past_days = past_days + 1
        for index, row in df.iterrows():
            if df.loc[index, 'date'] == date and df.loc[index, 'candlestick_pattern'] != 'NO_PATTERN':
                if past_days == 0:
                    w = str('********' + date + '********')
                    print(w)
                    w_str += str(w + ';\n')
                    if '_Bull' in str(df.loc[index, 'candlestick_pattern']):
                        score += 1
                    elif '_Bear' in str(df.loc[index, 'candlestick_pattern']):
                        score -= 1
                else:
                    w = str(date)
                    print(w)
                    w_str += str(w + ';\n')
                w = str(row)
                print(w)
                #w_str += str(w + ';\n')
                w = str('candlestick_pattern ranking: ' + str(candle_rankings[df.loc[index, 'candlestick_pattern']]))
                print(w)
                w_str += str(w + ';\n')
                print('----------------------------------------\n')
                pass

    return w_str, score
