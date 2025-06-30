import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import warnings
warnings.filterwarnings("ignore")

def train_and_forecast(sensor: str):
    # Load data
    df = pd.read_csv(r"C:\Users\32472\Desktop\sensor_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if sensor not in df.columns:
        print(f"Error: Column '{sensor}' not found.")
        return

    # Preprocess
    df = df[['timestamp', sensor]].dropna()
    df.set_index('timestamp', inplace=True)
    df = df.resample('H').mean().dropna()

    values = df[sensor].tolist()
    if len(values) < 20:
        print("Not enough data to train.")
        return

    # Train/test split
    split = int(0.8 * len(values))
    train = values[:split]
    test = values[split:]

    # Grid search over (p,d,q)
    best_cfg = None
    best_aic = float("inf")
    best_model = None

    print("Running manual grid search over SARIMAX(p,d,q)...")
    for p in range(3):
        for d in range(2):
            for q in range(3):
                try:
                    model = SARIMAX(train, order=(p, d, q), seasonal_order=(1, 0, 1, 24))
                    model_fit = model.fit(disp=False)
                    if model_fit.aic < best_aic:
                        best_aic = model_fit.aic
                        best_cfg = (p, d, q)
                        best_model = model_fit
                except:
                    continue

    if not best_model:
        print("Model training failed for all configurations.")
        return

    print(f"Best SARIMAX(p,d,q): {best_cfg}, AIC: {best_aic:.2f}")

    # Forecast
    forecast = best_model.forecast(steps=len(test))

    # Evaluation
    test = np.array(test)
    forecast = np.array(forecast)
    mask = ~np.isnan(test) & ~np.isnan(forecast)

    mae = mean_absolute_error(test[mask], forecast[mask])
    mse = mean_squared_error(test[mask], forecast[mask])
    mape = mean_absolute_percentage_error(test[mask], forecast[mask])

    print(f"\nEvaluation for {sensor.capitalize()}:")
    print(f"MAE: {mae:.3f}")
    print(f"MSE: {mse:.3f}")
    print(f"MAPE: {mape:.3f}")

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(test[mask], label='Actual')
    plt.plot(forecast[mask], label='Predicted')
    plt.title(f"SARIMAX Forecast for {sensor}")
    plt.xlabel("Time Step")
    plt.ylabel(sensor.capitalize())
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # For quick testing without argparse
    sensor = "temperature"  # or "humidity"
    train_and_forecast(sensor)

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description="SARIMAX Forecast for Sensor Data")
#    parser.add_argument('--sensor', type=str, choices=['temperature', 'humidity'], required=True,
#                        help="Sensor column name to model: 'temperature' or 'humidity'")
#    args = parser.parse_args()
#    train_and_forecast(args.sensor)

#python SarimaxTraining.py --sensor temperature