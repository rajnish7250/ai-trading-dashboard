def calculate_rsi(df):
    delta = df['Close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df


def generate_signal(last_predicted, last_actual, current_rsi):
    threshold = 1.003

    ml_buy = last_predicted > last_actual * threshold
    ml_sell = last_predicted < last_actual * (2 - threshold)

    rsi_buy = current_rsi < 30
    rsi_sell = current_rsi > 70

    if ml_buy and rsi_buy:
        return "BUY 📈 (Strong)"
    elif ml_sell and rsi_sell:
        return "SELL 📉 (Strong)"
    elif ml_buy:
        return "BUY 📈 (Weak)"
    elif ml_sell:
        return "SELL 📉 (Weak)"
    else:
        return "HOLD ⏳"