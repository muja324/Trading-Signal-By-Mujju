import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.title("📈 Stock Dashboard by Mujju")

# Sidebar input
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Fetch Data
@st.cache_data
def get_data(symbol, start, end):
    try:
        return yf.download(symbol, start=start, end=end)
    except Exception as e:
        st.error(f"Data fetch error: {e}")
        return pd.DataFrame()

df = get_data(symbol, start_date, end_date)

if not df.empty:
    st.subheader(f"{symbol} Closing Price")
    st.line_chart(df["Close"])

    st.subheader("📊 Technical Indicators")
    if ta:
        with st.spinner("Calculating indicators..."):
            try:
                df["SMA_20"] = df["Close"].rolling(window=20).mean()
                df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
                macd = ta.trend.MACD(df["Close"])
                df["MACD"] = macd.macd()

                st.line_chart(df[["Close", "SMA_20"]])
                st.line_chart(df[["RSI"]])
                st.line_chart(df[["MACD"]])

            except Exception as e:
                st.error(f"Indicator calculation failed: {e}")
else:
    st.warning("No data found for the given symbol and date range.")
