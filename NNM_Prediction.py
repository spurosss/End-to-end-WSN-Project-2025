#Run in Google Colab, couldnt download tensorflow

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from google.colab import files

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)


def create_dataset(series, window_size=10):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i + window_size])
        y.append(series[i + window_size])
    return np.array(X), np.array(y)


def load_and_prepare_data(csv_path, sensor_col='temperature', window_size=24):
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[['timestamp', sensor_col]].dropna()
    df.set_index('timestamp', inplace=True)

    df_resampled = df.resample('H').mean().dropna()
    data = df_resampled[sensor_col].values

    mean = data.mean()
    std = data.std()
    normalized_data = (data - mean) / std

    X, y = create_dataset(normalized_data, window_size)
    print(f"Data shapes - Features: {X.shape}, Targets: {y.shape}")
    return X, y, mean, std


def build_and_train_lstm(X_train, y_train, X_val, y_val, window_size, epochs=100, batch_size=32):
    model = Sequential()
    model.add(LSTM(50, input_shape=(window_size, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    callbacks = [
        EarlyStopping(patience=10, restore_best_weights=True),
        ModelCheckpoint("best_model.h5", save_best_only=True)
    ]

    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=1
    )

    model.save("lstm_temperature_model.h5")
    return model, history


def plot_training(history):
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_predictions(y_true, y_pred):
    plt.figure(figsize=(10, 5))
    plt.plot(y_true, label='Actual')
    plt.plot(y_pred, label='Predicted')
    plt.title('LSTM Predictions vs Actual')
    plt.xlabel('Time Step')
    plt.ylabel('Original Scale')
    plt.legend()
    plt.grid(True)
    plt.show()


def main(window_size=24):
    # Upload file from local machine 
    uploaded = files.upload()
    csv_path = list(uploaded.keys())[0]
    sensor_col = 'temperature'

    # Load and prepare data
    X, y, mean, std = load_and_prepare_data(csv_path, sensor_col, window_size)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Train/Val/Test split (70/10/20)
    total_size = len(X)
    train_size = int(total_size * 0.7)
    val_size = int(total_size * 0.1)

    X_train = X[:train_size - val_size]
    y_train = y[:train_size - val_size]
    X_val = X[train_size - val_size:train_size]
    y_val = y[train_size - val_size:train_size]
    X_test = X[train_size:]
    y_test = y[train_size:]

    # Train model
    model, history = build_and_train_lstm(X_train, y_train, X_val, y_val, window_size)

    # Plot training loss
    plot_training(history)

    # Predict and inverse scale
    y_pred = model.predict(X_test).flatten()
    y_pred_rescaled = y_pred * std + mean
    y_test_rescaled = y_test * std + mean

    # Plot predictions
    plot_predictions(y_test_rescaled, y_pred_rescaled)

    # Metrics on original scale
    mae = mean_absolute_error(y_test_rescaled, y_pred_rescaled)
    mse = mean_squared_error(y_test_rescaled, y_pred_rescaled)
    mape = mean_absolute_percentage_error(y_test_rescaled, y_pred_rescaled)
    accuracy = max(0, 1 - mape)

    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"MAPE: {mape:.4f}")
    print(f"Accuracy (1 - MAPE): {accuracy:.4f}")


if __name__ == "__main__":
    main(window_size=24)  
