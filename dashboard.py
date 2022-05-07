import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from breakout import is_breakingout,is_consolidating,is_breakdown

st.title('CHART DASHBOARD')

symbol = st.sidebar.text_input("TICKER",value="ADANIPORTS")
st.write(f"This is the chart of {symbol}")
file = r'stock_dfs_updated\{}.csv'.format(symbol)
df = pd.read_csv(file)
# st.dataframe(df)

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.update_xaxes(type='category')
fig.update_layout(height=800)
st.plotly_chart(fig,use_container_width=True)
# st.write(df)

consolidation=[]
squeeze=[]
for files in os.listdir('stock_dfs_updated'):
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

    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        squeeze.append(files)
    if is_consolidating(df):
        consolidation.append(files)
    else:
        pass
st.write("List of stock in consolidation phase",consolidation)
st.write("List of stock coming out of squeeze phase",squeeze)