
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import joblib

st.title("📈 AI/ML Trading Signal Generator")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")

@st.cache_data
def get_data(ticker):
    df = yf.download(ticker, period="6mo")

    if df.empty or 'Close' not in df.columns:
        return pd.DataFrame()

    df = df.dropna()

    # ✅ Ensure Close is 1D Series
    close_series = df['Close'].squeeze()

    try:
        df['rsi'] = ta.momentum.RSIIndicator(close=close_series).rsi()
        df['sma_20'] = ta.trend.SMAIndicator(close=close_series, window=20).sma_indicator()
        df['macd'] = ta.trend.MACD(close=close_series).macd()
    except Exception as e:
        st.error(f"Indicator calculation error: {e}")
        return pd.DataFrame()

    df = df.dropna()
    return df

if ticker:
    df = get_data(ticker)

    if df.empty:
        st.error("❌ Failed to fetch or process data. Please check the ticker symbol.")
    else:
        try:
            X = df[['rsi', 'sma_20', 'macd']]
            model = joblib.load("model.pkl")

            df['prediction'] = model.predict(X)
            df['Buy_Signal'] = df['prediction'].apply(lambda x: 'BUY' if x == 1 else '')

            st.subheader("📊 Latest Buy Signals")
            st.dataframe(df[['Close', 'rsi', 'Buy_Signal']].tail(10))
        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
