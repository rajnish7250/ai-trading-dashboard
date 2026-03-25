def execute_trade(signal, state, current_price):
    if signal.startswith("BUY") and state["shares"] == 0:
        state["shares"] = state["balance"] / current_price
        state["balance"] = 0
        state["trade_log"].append(f"BUY at {current_price:.2f}")

    elif signal.startswith("SELL") and state["shares"] > 0:
        state["balance"] = state["shares"] * current_price
        state["shares"] = 0
        state["trade_log"].append(f"SELL at {current_price:.2f}")

    return state