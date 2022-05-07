import os
import pandas as pd
import requests

webhook_url = "https://discord.com/api/webhooks/972496453140353074/EetCM63GWYTGIANyLZiozFXcZ__Lwr0FmRNb0e-JZClPDDBwiVNz3BbiPaQVvC-y7szN"

squeeze = []
for files in os.listdir('stock_dfs_updated'):
    symbol = files.split(".")[0]
    df = pd.read_csv('stock_dfs_updated/{}'.format(files))
    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']


    df['squeeze_on'] = df.apply(in_squeeze, axis=1)
    # print(df)
    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        squeeze.append(files)
        msg=f"{symbol} Stock is coming out of TTM squeeze"
        print(msg)
        payload={
            "username":"AKJ",
            "content":msg
        }
        requests.post(webhook_url, json=payload)
    else:
        pass
