import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data import load_data
from model import train_model
from strategy import calculate_rsi, generate_signal
from trading import execute_trade

st.title("📈 Stock Dashboard")

ticker = st.text_input("Enter Stock", "AAPL")

df = load_data(ticker, "2020-01-01", "2024-01-01")

if df.empty:
    st.error("No data found")
    st.stop()

# RSI
df = calculate_rsi(df)
current_rsi = df['RSI'].iloc[-1]

# ---------------------------
# ML MODEL (MOVE UP 🔥)
# ---------------------------
predictions, actual = train_model(df)

last_predicted = predictions[-1][0]
last_actual = actual[-1][0]
current_price = df['Close'].iloc[-1]

# ---------------------------
# CHARTS
# ---------------------------
st.markdown("## 📊 Market Analysis")

# Price Chart
st.subheader("📈 Closing Price Chart")
st.line_chart(df['Close'])

# Moving Average
st.subheader("📉 Moving Average (50 days)")
df['MA50'] = df['Close'].rolling(50).mean()
st.line_chart(df[['Close', 'MA50']])

# RSI Chart
st.subheader("📊 RSI Indicator")
st.line_chart(df['RSI'])

# Prediction vs Actual
st.subheader("🤖 Prediction vs Actual")

fig, ax = plt.subplots()
ax.plot(actual, label="Actual")
ax.plot(predictions, label="Predicted")
ax.legend()

st.pyplot(fig)

# ---------------------------
# SIGNAL
# ---------------------------
signal = generate_signal(last_predicted, last_actual, current_rsi)

st.write(f"Signal: {signal}")
st.write(f"RSI: {current_rsi:.2f}")

# ---------------------------
# SESSION STATE
# ---------------------------
if "state" not in st.session_state:
    st.session_state.state = {
        "balance": 10000,
        "shares": 0,
        "trade_log": []
    }

# ---------------------------
# TRADING
# ---------------------------
if st.button("Run Trade"):
    st.session_state.state = execute_trade(
        signal,
        st.session_state.state,
        current_price
    )

# ---------------------------
# DISPLAY
# ---------------------------
state = st.session_state.state
total = state["balance"] + (state["shares"] * current_price)

st.write(f"Balance: {state['balance']:.2f}")
st.write(f"Shares: {state['shares']:.2f}")
st.write(f"Total: {total:.2f}")
st.write(state["trade_log"])