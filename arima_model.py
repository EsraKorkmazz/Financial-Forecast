import streamlit as st
from utils import get_stock_data, stocks
import pandas as pd
from datetime import timedelta
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression():
    stock_name = st.selectbox("Lütfen tahmin etmek istediğiniz hisse senedini seçin (Lineer Regresyon):", list(stocks.keys()), key='linear_regression_selectbox')
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            st.write("### Lineer Regresyon Tahmin Sonuçları")
            steps = st.slider("Tahmin Edilmesini istediğiniz gün sayısını seçin (Lineer Regresyon)", min_value=1, max_value=30, value=7, key='linear_regression_slider')
            
            if st.button("Lineer Regresyon ile Tahmin Et"):
                data['Date'] = pd.to_datetime(data.index)
                data['Date_ordinal'] = data['Date'].map(pd.Timestamp.toordinal)
                
                X = data['Date_ordinal'].values.reshape(-1, 1)
                y = data['Close'].values.reshape(-1, 1)
                
                model = LinearRegression()
                model.fit(X, y)
                
                future_dates = [data['Date'].max() + timedelta(steps) for steps in range(1, steps + 1)]
                future_dates_ordinal = np.array([date.toordinal() for date in future_dates]).reshape(-1, 1)
                future_predictions = model.predict(future_dates_ordinal)
                
                forecast_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Close'])
                
                st.write(f"### {steps} Günlük Tahmin (Lineer Regresyon)")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Gerçek fiyat'))
                fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Close'], mode='lines', name='Gelecek fiyat tahmini'))
                fig.update_layout(title=f'{stock_name} Hisse Senedi Tahmini (Lineer Regresyon)', xaxis_title='Tarih', yaxis_title='Fiyat')
                st.plotly_chart(fig)

                st.write(forecast_df)
                
        else:
            st.write("Veri alınamadı. Lütfen geçerli bir sembol seçin.")

def show_arima_model():
    stock_name = st.selectbox("Lütfen tahmin etmek istediğiniz hisse senedini seçin:", list(stocks.keys()), key='arima_selectbox')
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            st.write("### ARIMA Tahmin Sonuçları")
            steps = st.slider("Tahmin Edilmesini istediğiniz gün sayısını seçi (ARIMA)", min_value=1, max_value=30, value=7, key='arima_slider')
            
            if st.button("Tahmin Et"):
                p, d, q = 15, 1, 5  # Sabit parametreler
                model = ARIMA(data['Close'], order=(p, d, q))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=steps)
                
                # Orijinal veri setinin son tarihinden bir gün sonrasından başlayarak tahmin edilen gün sayısını ekleyerek tarih dizisi oluştur
                forecast_index = pd.date_range(start=data.index[-1] + timedelta(days=1), periods=steps, freq='D')
                forecast_df = pd.DataFrame(forecast.values, index=forecast_index, columns=['Tahmini Fiyat'])
                forecast_df.index = forecast_df.index.strftime('%Y-%m-%d')
                
                # Combine the real and forecasted data
                combined_df = pd.concat([data[['Close']], forecast_df.rename(columns={'Tahmini Fiyat': 'Close'})])
                

                st.write(f"### {steps} Günlük Tahmin")
            
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Gerçek fiyat'))
                fig.add_trace(go.Scatter(x=forecast_index, y=forecast, mode='lines', name='Gelecek fiyat tahmini'))
                fig.update_layout(title=f'{stock_name} Hisse Senedi Tahmini', xaxis_title='Tarih', yaxis_title='Fiyat')
                st.plotly_chart(fig)

                st.write(forecast_df)

                # Save forecast_df to CSV on Desktop
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "forecast_data.csv")
                combined_df.to_csv(desktop_path)
                st.success(f"Tahmin verileri {desktop_path} konumuna kaydedildi.")
                print(f"Tahmin verileri {desktop_path} konumuna kaydedildi.")  # Debugging statement




        else:
            st.write("Veri alınamadı. Lütfen geçerli bir sembol seçin.")