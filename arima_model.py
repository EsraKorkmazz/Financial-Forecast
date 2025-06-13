import streamlit as st
from utils import get_stock_data, stocks
import pandas as pd
from datetime import timedelta
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
import numpy as np
import os

def linear_regression():
    stock_name = st.selectbox("Select the stock you want to predict (Linear Regression):", list(stocks.keys()), key='linear_regression_selectbox')
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            st.write("### Linear Regression Prediction Results")
            steps = st.slider("Select the number of days to predict (Linear Regression)", min_value=1, max_value=30, value=7, key='linear_regression_slider')
            
            if st.button("Predict with Linear Regression"):
                data['Date'] = pd.to_datetime(data.index)
                data['Date_ordinal'] = data['Date'].map(pd.Timestamp.toordinal)
                
                X = data['Date_ordinal'].values.reshape(-1, 1)
                y = data['Close'].values.reshape(-1, 1)
                
                model = LinearRegression()
                model.fit(X, y)
                
                future_dates = [data['Date'].max() + timedelta(days=step) for step in range(1, steps + 1)]
                future_dates_ordinal = np.array([date.toordinal() for date in future_dates]).reshape(-1, 1)
                future_predictions = model.predict(future_dates_ordinal)
                
                forecast_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Close'])
                
                st.write(f"### {steps}-Day Prediction (Linear Regression)")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Price'))
                fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Close'], mode='lines', name='Predicted Future Price'))
                fig.update_layout(title=f'{stock_name} Stock Price Prediction (Linear Regression)', xaxis_title='Date', yaxis_title='Price')
                st.plotly_chart(fig)

                st.write(forecast_df)
                
        else:
            st.write("Data not found. Please select a valid symbol.")

def show_arima_model():
    stock_name = st.selectbox("Select the stock you want to predict (ARIMA):", list(stocks.keys()), key='arima_selectbox')
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            st.write("### ARIMA Prediction Results")
            steps = st.slider("Select the number of days to predict (ARIMA)", min_value=1, max_value=30, value=7, key='arima_slider')
            
            if st.button("Predict"):
                p, d, q = 15, 1, 5  # Fixed parameters
                model = ARIMA(data['Close'], order=(p, d, q))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=steps)
                
                forecast_index = pd.date_range(start=data.index[-1] + timedelta(days=1), periods=steps, freq='D')
                forecast_df = pd.DataFrame(forecast.values, index=forecast_index, columns=['Predicted Price'])
                forecast_df.index = forecast_df.index.strftime('%Y-%m-%d')
                
                combined_df = pd.concat([data[['Close']], forecast_df.rename(columns={'Predicted Price': 'Close'})])
                
                st.write(f"### {steps}-Day Prediction")
            
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Price'))
                fig.add_trace(go.Scatter(x=forecast_index, y=forecast, mode='lines', name='Predicted Future Price'))
                fig.update_layout(title=f'{stock_name} Stock Price Prediction', xaxis_title='Date', yaxis_title='Price')
                st.plotly_chart(fig)

                st.write(forecast_df)

                # Save forecast_df to CSV on Desktop
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "forecast_data.csv")
                combined_df.to_csv(desktop_path)
                st.success(f"Prediction data saved to {desktop_path}.")
                print(f"Prediction data saved to {desktop_path}.")  # Debugging statement

        else:
            st.write("Data not found. Please select a valid symbol.")
