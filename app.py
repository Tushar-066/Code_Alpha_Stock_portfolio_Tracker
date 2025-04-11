import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Portfolio Tracker", layout="centered")
st.title("📊 Stock Portfolio Tracker")

# Session state for storing portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

# Input form
with st.form("stock_form", clear_on_submit=True):
    ticker = st.text_input("Stock Ticker (e.g., AAPL, MSFT)").upper()
    quantity = st.number_input("Quantity", min_value=1)
    buy_price = st.number_input("Buy Price", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add to Portfolio")
    if submitted and ticker:
        st.session_state.portfolio.append({
            "ticker": ticker,
            "quantity": quantity,
            "buy_price": buy_price
        })

# Display portfolio
if st.session_state.portfolio:
    st.subheader("📈 Portfolio Summary")

    data = []
    total_invested = 0
    total_value = 0

    for stock in st.session_state.portfolio:
        ticker = stock["ticker"]
        qty = stock["quantity"]
        buy_price = stock["buy_price"]
        try:
            current_price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
        except:
            current_price = 0.0
        current_value = current_price * qty
        invested = qty * buy_price
        profit = current_value - invested

        total_invested += invested
        total_value += current_value

        data.append([
            ticker, qty, f"${buy_price:.2f}", f"${current_price:.2f}",
            f"${current_value:.2f}", f"${profit:.2f}"
        ])

    df = pd.DataFrame(data, columns=[
        "Ticker", "Quantity", "Buy Price", "Current Price", "Current Value", "P/L"
    ])
    st.dataframe(df, use_container_width=True)

    st.markdown(f"**💰 Total Invested:** ${total_invested:.2f}")
    st.markdown(f"**📦 Current Portfolio Value:** ${total_value:.2f}")
    st.markdown(f"**📈 Overall Profit/Loss:** ${total_value - total_invested:.2f}")
else:
    st.info("Add a stock above to get started!")

