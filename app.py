import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import os

# Optional: install ta only if technical indicators are used
try:
    import ta
except ImportError:
    ta = None

os.environ["YFINANCE_NO_CACHE"] = "true"

st.set_page_config(page_title="📊 Stock Viewer by Mujahidul", layout="wide")
st.title("📈 Stock Chart & Indicators Viewer")

# Sidebar inputs
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL or TATASTEEL.NS)", "AAPL").upper()
today = dt.date.today()
one_year_ago = today - dt.timedelta(days=365)
start = st.sidebar.date_input("Start Date", one_year_ago)
end = st.sidebar.date_input("End Date", today)

# Validate dates
if start >= end:
    st.error("⚠️ End date must be after start date.")
    st.stop()

# Fetch data
if ta:
    try:
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
        macd = ta.trend.MACD(df["Close"])
        df["MACD"] = macd.macd()
    except Exception as e:
        st.error(f"Indicator calculation failed: {e}")

st.success(f"✅ Showing data for {symbol} from {start} to {end}")
st.dataframe(df.tail())

# Plot basic charts
st.subheader("📉 Price Charts")
st.line_chart(df["Close"], height=300)
st.line_chart(df["Volume"], height=150)

# Calculate Indicators
if ta:
    try:
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
macd = ta.trend.MACD(df["Close"])
df["MACD"] = macd.macd()

        st.subheader("📊 Technical Indicators")
        st.line_chart(df[["Close", "SMA_20"]])
        st.line_chart(df["RSI"])
        st.line_chart(df["MACD"])
    except Exception as e:
        st.warning(f"⚠️ Indicator calculation error: {e}")
else:
    st.info("📦 Technical indicators not installed. Add `ta` to requirements if needed.")
