from openai import OpenAI
import streamlit as st
import matplotlib.pyplot as plt
from utils import get_stock_data, stocks
import os
from dotenv import load_dotenv

api_key='YOUR_API_KEY'

# OpenAI API anahtarınızı buraya ekleyin
client = OpenAI(api_key=api_key)

def show_reporting():
    st.write("### Raporlama")
    stock_name = st.selectbox("Raporlama yapmak istediğiniz hisse senedini seçin:", list(stocks.keys()))
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            average_price = data["Close"].mean()
            median_price = data["Close"].median()
            std_dev = data["Close"].std()
            min_price = data["Close"].min()
            max_price = data["Close"].max()

            # Karar Önerileri
            st.write("### Karar Önerileri")
            
            gpt_prompt = (
                f"Bir hisse senedi analizi yapıyorsunuz. İşte {stock_name} için temel analiz sonuçları:\n\n"
                f"Bu verilere göre, kullanıcıya {stock_name} hisse senedini alması veya almaması gerektiği konusunda ne önerirsiniz? Nedenleriyle birlikte açıklayın."
                f"Sadece al veya alma olarak cıktı ver."
            )
            
            if st.button("GPT Analizini Al"):
                response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Daha uygun maliyetli model olarak GPT-3.5-Turbo kullanılıyor
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": gpt_prompt}
                ],
                max_tokens=500  # Yanıtın uzunluğunu sınırlandırmak için
            )
                st.write("### GPT Karar Önerisi")
                response_message = response.choices[0].message.content
                st.write(response_message)
            # Görselleştirmeler
            st.write("### Görselleştirmeler")
            
            # Kapanış Fiyatı Zaman Serisi
            st.write("**Kapanış Fiyatı Zaman Serisi**")
            plt.figure(figsize=(10, 5))
            plt.plot(data['Close'], label='Kapanış Fiyatı')
            plt.title(f'{stock_name} Kapanış Fiyatı')
            plt.xlabel('Tarih')
            plt.ylabel('Kapanış Fiyatı')
            plt.legend()
            st.pyplot(plt)
            
            # Kapanış Fiyatları Histogramı
            st.write("**Kapanış Fiyatları Histogramı**")
            plt.figure(figsize=(10, 5))
            plt.hist(data['Close'], bins=50, alpha=0.7)
            plt.title(f'{stock_name} Kapanış Fiyatı Dağılımı')
            plt.xlabel('Kapanış Fiyatı')
            plt.ylabel('Frekans')
            st.pyplot(plt)
            
            # Kapanış Fiyatları Kutu Grafiği
            st.write("**Kapanış Fiyatları Kutu Grafiği**")
            plt.figure(figsize=(10, 5))
            plt.boxplot(data['Close'])
            plt.title(f'{stock_name} Kapanış Fiyatı Kutu Grafiği')
            plt.ylabel('Kapanış Fiyatı')
            st.pyplot(plt)

            
        else:
            st.write("Veri alınamadı. Lütfen geçerli bir sembol seçin.")

