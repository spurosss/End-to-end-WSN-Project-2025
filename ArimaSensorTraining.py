import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


def main():
    # Load the CSV file
    df = pd.read_csv(r"C:\Users\32472\Desktop\sensors\sensor_data.csv")

    # Convert 'timestamp' column to datetime64
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create a new DataFrame with only 'timestamp' and 'temperature'
    temperature_df = df[['timestamp', 'temperature']]

    # Set 'timestamp' as index
    temperature_df.set_index('timestamp', inplace=True)

    # Resample to hourly and take the mean
    temperature_df_hourly = temperature_df.resample('h').mean()

    # Drop rows with missing temperature values (NaNs)
    temperature_df_hourly.dropna(inplace=True)

    # Create a list of temperature values
    temperature = temperature_df_hourly['temperature'].tolist()

    # Ensure there's enough data
    if len(temperature) < 10:
        print("Not enough data after cleaning to train/test ARIMA.")
        return

    # Split the dataset (80% train, 20% test)
    split_idx = int(len(temperature) * 0.8)
    train = temperature[:split_idx]
    test = temperature[split_idx:]

    # Fit the ARIMA model
    model = ARIMA(train, order=(2, 1, 2))
    model_fit = model.fit()

    # Forecast the same number of steps as the test set
    forecast = model_fit.forecast(steps=len(test))

    # Drop any NaNs from forecast or test (just in case)
    forecast = np.array(forecast)
    test = np.array(test)
    mask = ~np.isnan(forecast) & ~np.isnan(test)

    # Plot Actual vs Predicted values
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(test[mask])), test[mask], label='Actual')
    plt.plot(range(len(forecast[mask])), forecast[mask], label='Predicted')
    plt.legend(['Actual', 'Predicted'])
    plt.title('ARIMA Forecast vs Actual')
    plt.xlabel('Time Step')
    plt.ylabel('Temperature')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Calculate and print performance metrics
    mae = mean_absolute_error(test[mask], forecast[mask])
    mse = mean_squared_error(test[mask], forecast[mask])
    mape = mean_absolute_percentage_error(test[mask], forecast[mask])

    print(f"MAE: {mae:.3f}")
    print(f"MSE: {mse:.3f}")
    print(f"MAPE: {mape:.3f}")


if __name__ == "__main__":
    main()