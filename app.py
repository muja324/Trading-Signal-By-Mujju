
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import joblib

st.title("AI/ML Trading Signal Generator")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")

@st.cache_data
def get_data(ticker):
    df = yf.download(ticker, period="6mo")
    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['sma_20'] = ta.trend.SMAIndicator(df['Close'], 20).sma_indicator()
    df['macd'] = ta.trend.MACD(df['Close']).macd()
    df = df.dropna()
    return df

if ticker:
    df = get_data(ticker)
    X = df[['rsi', 'sma_20', 'macd']]
    model = joblib.load("model.pkl")

    df['prediction'] = model.predict(X)
    df['Buy_Signal'] = df['prediction'].apply(lambda x: 'BUY' if x == 1 else '')

    st.subheader("Latest Buy Signals")
    st.dataframe(df[['Close', 'rsi', 'Buy_Signal']].tail(10))
