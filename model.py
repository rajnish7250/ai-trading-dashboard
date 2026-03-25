import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def train_model(df):
    data = df[['Close']]

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []

    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i])
        y.append(scaled_data[i])

    X, y = np.array(X), np.array(y)

    split = int(0.8 * len(X))

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(60,1)))
    model.add(LSTM(50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=2, batch_size=32, verbose=0)

    predictions = model.predict(X_test)

    predictions = scaler.inverse_transform(predictions)
    y_test_actual = scaler.inverse_transform(y_test)

    return predictions, y_test_actual