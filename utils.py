import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import timedelta
import streamlit as st

stocks = {
    "Türk Hava Yolları": "THYAO.IS",
    "ASELSAN": "ASELS.IS",
    "Garanti Bankası": "GARAN.IS",
    "Koç Holding": "KCHOL.IS",
    "Ford Otosan": "FROTO.IS",
    "Ereğli Demir Çelik": "EREGL.IS",
    "Şişe Cam": "SISE.IS",
    "Akbank": "AKBNK.IS",
    "Sabancı Holding": "SAHOL.IS",
    "Tüpraş": "TUPRS.IS",
    "Petkim": "PETKM.IS",
    "Bim": "BIMAS.IS",
    "Yapı Kredi": "YKBNK.IS",
    "Tofaş": "TOASO.IS",
    "Arçelik": "ARCLK.IS",
    "Turkcell": "TCELL.IS",
    "Vakıfbank": "VAKBN.IS",
    "Enka İnşaat": "ENKAI.IS",
    "Tekfen Holding": "TKFEN.IS",
    "Türk Telekom": "TTKOM.IS",
    "İş Bankası": "ISCTR.IS",
    "Migros": "MGROS.IS",
    "Halkbank": "HALKB.IS",
    "Otokar": "OTKAR.IS",
    "Albaraka Türk": "ALBRK.IS",
    "Doğan Holding": "DOHOL.IS",
    "GSD Holding": "GSDHO.IS",
    "Zorlu Enerji": "ZOREN.IS",
    "Karsan": "KARSN.IS",
    "Gübre Fabrikaları": "GUBRF.IS",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Tesla": "TSLA"
}

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="1y")
        return df
    except Exception as e:
        st.error(f"Veri işlenirken bir hata oluştu: {e}")
        return None
    
def plot_forecast(data, forecast, mean_value, steps):
    forecast_index = pd.date_range(start=data.index[-1] + timedelta(days=1), periods=steps, freq='D')
    forecast_series = pd.Series(forecast.flatten(), index=forecast_index)
    
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Gerçek fiyat')
    plt.plot(forecast_series, label='Gelecek fiyat tahmini')
    plt.axhline(y=mean_value, color='r', linestyle='--', label='Ortalama')
    plt.legend()
    st.pyplot(plt)


def plot_moving_average(data, window):
    data['Moving Average'] = data['Close'].rolling(window=window).mean()
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['Moving Average'], label=f'{window}-Day Moving Average')
    plt.legend()
    st.pyplot(plt)
    


