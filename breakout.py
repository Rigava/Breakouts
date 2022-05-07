import os
import pandas as pd

webhook_url = "https://discord.com/api/webhooks/970262509963591731/dlo67rPlslfcW516HAQlhy80YYk7RAaxKyDmV7CLnjaodmA2ebfqxMJy6OmJMdGt8xxd"


def is_consolidating(data):
    recent_candles = data[-15:]
    max_close = recent_candles['Close'].max()
    min_close = recent_candles['Close'].min()
    # print('the max close was {} and the min close was {}'.format(max_close,min_close))
    if min_close > (max_close * 0.96):
        return True
    return False


def is_breakingout(data):
    last_close = data[-1:]['Close'].values[0]
    if is_consolidating(data[:-1]):
        recent_candles = data[-16:-1]
        if last_close > recent_candles['Close'].max():
            return True
    return False


def is_breakdown(data):
    last_close = data[-1:]['Close'].values[0]
    if is_consolidating(data[:-1]):
        recent_candles = data[-16:-1]
        if last_close < recent_candles['Close'].min():
            return True
    return False


for filename in os.listdir(file):
    df = pd.read_csv(r'stock_dfs_updated\{}'.format(filename))
    if is_consolidating(df):
        print("{} is consolidating".format(filename))
    if is_breakdown(df):
        print("{} is breaking down".format(filename))
    if is_breakingout(df):
        print("{} is breaking out".format(filename))
