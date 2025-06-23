import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="Trading Dashboard by Mujju", layout="wide")

st.title("📈 Stock Analysis Dashboard by Mujju")

# Sidebar for inputs
symbol = st.sidebar.text_input("Enter Stock Symbol:", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Fetch stock data
@st.cache_data
def load_data(symbol, start, end):
    try:
        data = yf.download(symbol, start=start, end=end)
        return data
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        return pd.DataFrame()

df = load_data(symbol, start_date, end_date)

# Show data or warning
if df.empty:
    st.warning("No data found for the selected symbol and date range.")
else:
    st.subheader(f"{symbol} Closing Price")
    st.line_chart(df["Close"])

    # Technical Indicators
    if ta:
        with st.spinner("📊 Calculating indicators..."):
            try:
                df["SMA_20"] = df["Close"].rolling(window=20).mean()
                df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

                macd = ta.trend.MACD(df["Close"])

                macd_values = macd.macd()
                if isinstance(macd_values, pd.DataFrame):
                    macd_values = macd_values.iloc[:, 0]
                df["MACD"] = macd_values

                signal_values = macd.signal()
                if isinstance(signal_values, pd.DataFrame):
                    signal_values = signal_values.iloc[:, 0]
                df["MACD_Signal"] = signal_values

                # Charts
                st.subheader("📉 SMA + Close Price")
                st.line_chart(df[["Close", "SMA_20"]])

                st.subheader("📈 RSI")
                st.line_chart(df[["RSI"]])

                st.subheader("🔁 MACD & Signal")
                st.line_chart(df[["MACD", "MACD_Signal"]])

            except Exception as e:
                st.error(f"Indicator calculation failed: {e}")
