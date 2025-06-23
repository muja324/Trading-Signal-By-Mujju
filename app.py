import streamlit as st
import pandas as pd
import yfinance as yf
import ta

st.set_page_config(page_title="Trading Dashboard by Mujju", layout="wide")
st.title("📈 Stock Analysis Dashboard by Mujju")

# Sidebar Inputs
symbol = st.sidebar.text_input("Enter Stock Symbol:", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Load data
@st.cache_data
def load_data(symbol, start, end):
    try:
        data = yf.download(symbol, start=start, end=end)
        return data
    except Exception as e:
        st.error(f"Data load error: {e}")
        return pd.DataFrame()

df = load_data(symbol, start_date, end_date)

# Display price chart
if df.empty:
    st.warning("⚠️ No data found. Try another symbol or date range.")
else:
    st.subheader(f"{symbol} Closing Price")
    st.line_chart(df["Close"])

    # Technical Indicator Calculation
    if ta:
        with st.spinner("📊 Calculating indicators..."):
            try:
                # SMA & RSI
                df["SMA_20"] = df["Close"].rolling(window=20).mean()
                df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

                # MACD & Signal with bulletproof shape handling
                macd = ta.trend.MACD(df["Close"])

                def ensure_series(data):
                    if isinstance(data, pd.DataFrame):
                        return data.iloc[:, 0]
                    elif isinstance(data, (pd.Series, list, tuple)):
                        return pd.Series(data)
                    elif hasattr(data, "squeeze"):
                        return pd.Series(data.squeeze())
                    else:
                        raise ValueError("Unsupported MACD format")

                df["MACD"] = ensure_series(macd.macd())
                df["MACD_Signal"] = ensure_series(macd.signal())

                # Charts
                st.subheader("📉 SMA + Close")
                st.line_chart(df[["Close", "SMA_20"]])

                st.subheader("📈 RSI")
                st.line_chart(df[["RSI"]])

                st.subheader("🔁 MACD & Signal")
                st.line_chart(df[["MACD", "MACD_Signal"]])

            except Exception as e:
                st.error(f"Indicator calculation failed: {e}")
