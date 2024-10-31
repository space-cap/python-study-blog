import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykrx import stock
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime, timedelta


def get_stock_data(ticker: str, start_date: str, end_date: str):
    """
    Fetches OHLCV and fundamental indicators for a given stock ticker.

    Parameters:
    - ticker: str
        The stock ticker symbol to fetch data for.
    - start_date: str
        The start date for fetching data in 'YYYYMMDD' format.
    - end_date: str
        The end date for fetching data in 'YYYYMMDD' format.

    Returns:
    - DataFrame:
        A DataFrame containing OHLCV and fundamental indicators.
    """
    # Fetch OHLCV data
    ohlcv = stock.get_market_ohlcv(start_date, end_date, ticker)

    # Fetch fundamental data
    fundamentals = stock.get_market_fundamental(start_date, end_date, ticker)

    # Combine OHLCV and fundamental data
    combined_data = ohlcv.join(fundamentals[['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']], how='inner')
    return combined_data


def prepare_data(data: pd.DataFrame, feature_col: str, target_col: str):
    """
    Prepares the data for LSTM model training.

    Parameters:
    - data: DataFrame
        The DataFrame containing the stock data.
    - feature_col: str
        The column name to be used as features.
    - target_col: str
        The column name to be used as the target.

    Returns:
    - X: np.array
        The feature data for LSTM.
    - y: np.array
        The target data for LSTM.
    """
    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[[feature_col]].values)

    # Prepare the dataset for LSTM
    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i - 60:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM
    return X, y, scaler


def build_lstm_model(input_shape: tuple):
    """
    Builds and compiles the LSTM model.

    Parameters:
    - input_shape: tuple
        The shape of the input data for the LSTM model.

    Returns:
    - model: Sequential
        The compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # Prediction of the next closing price
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def predict_future_prices(model, scaler, last_60_days: np.array):
    """
    Predicts future prices using the trained LSTM model.

    Parameters:
    - model: Sequential
        The trained LSTM model.
    - scaler: MinMaxScaler
        The scaler used to scale the data.
    - last_60_days: np.array
        The last 60 days of stock prices for prediction.

    Returns:
    - predicted_prices: np.array
        The predicted prices for the next week.
    """
    # Prepare the last 60 days data for prediction
    last_60_days_scaled = scaler.transform(last_60_days)
    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Predicting the next 7 days
    predicted_prices = model.predict(X_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)  # Inverse scaling
    return predicted_prices


def visualize_predictions(actual_prices: np.array, predicted_prices: np.array):
    """
    Visualizes the actual vs predicted stock prices.

    Parameters:
    - actual_prices: np.array
        The actual stock prices.
    - predicted_prices: np.array
        The predicted stock prices.
    """
    plt.figure(figsize=(14, 5))
    plt.plot(actual_prices, color='blue', label='Actual Prices')
    plt.plot(predicted_prices, color='red', label='Predicted Prices')
    plt.title('Stock Price Prediction')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


# Main execution
if __name__ == "__main__":
    # Define the ticker and date range
    ticker = '005930'  # Samsung Electronics
    today = datetime.now()
    start_date = (today - timedelta(days=365)).strftime('%Y%m%d')
    end_date = today.strftime('%Y%m%d')

    # Get stock data
    stock_data = get_stock_data(ticker, start_date, end_date)

    # Prepare data for LSTM
    X, y, scaler = prepare_data(stock_data, 'Close', 'Close')

    # Build and train the LSTM model
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=50, batch_size=32)

    # Predict future prices
    last_60_days = stock_data['Close'].values[-60:]
    predicted_prices = predict_future_prices(model, scaler, last_60_days)

    # Visualize the predictions
    visualize_predictions(stock_data['Close'].values[-7:], predicted_prices)