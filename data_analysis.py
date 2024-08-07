import streamlit as st
import pandas as pd
from utils import get_stock_data, stocks, plot_moving_average
import plotly.graph_objs as go

def show_data_analysis():
    st.write("### Veri Analizi")
    stock_name = st.selectbox("Lütfen analiz etmek istediğiniz hisse senedini seçin:", list(stocks.keys()))
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            st.write("### Yüklenen Veri")
            #Burada tabloda maksimum degerler renklendirildi
            def highlight_max(s):
                '''
                Sütunun maksimum değerine göre satırları renklendirme
                '''
                is_max = s == s.max()
                return ['background-color: red' if v else '' for v in is_max]
            # Veriyi sıralama ve filtreleme
            #Filtreleme eklendi(open,high,low,close tiklandiginda en yuksel ve en dusuk deger tablonun basinda gosteriliyor.
            sorted_data = data.sort_values(by='Date', ascending=False)
            filtered_data = sorted_data[sorted_data['Close'] > 105]
            styled_data = filtered_data.style.apply(highlight_max, subset=['Open', 'Close', 'Volume'], axis=0)
            st.dataframe(styled_data)

            st.write("### Veri İstatistikleri")
            st.write(data.describe())
            st.write("### Zaman Serisi Grafiği")
            fig_close = go.Figure()
            fig_close.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Kapanış Fiyatı'))
            st.plotly_chart(fig_close)

            st.write("### Hacim Grafiği")
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Hacim'))
            st.plotly_chart(fig_volume)
            
            st.write("### Hareketli Ortalama Hesaplama")
            window = st.slider("Hareketli Ortalama Süresi (Gün)", min_value=1, max_value=50, value=20)
            plot_moving_average(data, window)
            
            #MACD, RSI, BOLLINGER ICIN INDICATOR
            st.write("### Gösterge Seçimi")
            indicator = st.selectbox("Lütfen analiz etmek istediğiniz göstergeleri seçin:", ["MACD", "RSI", "BOLLINGER"])
            
            def plot_macd(data):
                exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                macd = exp1 - exp2
                signal = macd.ewm(span=9, adjust=False).mean()

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=macd, mode='lines', name='MACD', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=data.index, y=signal, mode='lines', name='Signal Line', line=dict(color='red')))
                fig.update_layout(title='MACD', xaxis_title='Date', yaxis_title='MACD Value')
                st.plotly_chart(fig)

                # MACD gauge chart
                latest_macd = macd.iloc[-1]
                latest_signal = signal.iloc[-1]

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=latest_macd,
                    title={'text': "MACD Değeri"},
                    gauge={
                        'axis': {'range': [-5, 5]},
                        'steps': [
                            {'range': [-5, 0], 'color': "lightgray"},
                            {'range': [0, 5], 'color': "lightgreen"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': latest_macd}}))
                st.plotly_chart(fig_gauge)
                
                # Al/Sat önerisi
                if latest_macd > latest_signal:
                    recommendation = "AL"
                    recommendation_color = "green"
                else:
                    recommendation = "SAT"
                    recommendation_color = "red"

                st.write(f"### Öneri: {recommendation}")

                fig_recommendation = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=latest_macd,
                    number={'prefix': f"{recommendation} - "},
                    delta={'position': "top", 'reference': latest_signal},
                    title={"text": "Al/Sat Önerisi"},
                    domain={'x': [0, 1], 'y': [0, 1]}
                ))
                fig_recommendation.update_layout(
                    paper_bgcolor=recommendation_color,
                    font={'color': "white"}
                )
                st.plotly_chart(fig_recommendation)

            def plot_rsi(data, window=14):
                delta = data['Close'].diff(1)
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(window=window).mean()
                avg_loss = loss.rolling(window=window).mean()
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=rsi, mode='lines', name='RSI'))
                fig.add_shape(type="line", x0=data.index[0], y0=70, x1=data.index[-1], y1=70, line=dict(color="red", width=1, dash="dash"), name="Overbought")
                fig.add_shape(type="line", x0=data.index[0], y0=30, x1=data.index[-1], y1=30, line=dict(color="green", width=1, dash="dash"), name="Oversold")
                fig.update_layout(title='RSI', xaxis_title='Date', yaxis_title='RSI Value')
                st.plotly_chart(fig)

                # RSI gauge chart
                latest_rsi = rsi.iloc[-1]

                # Öneri belirleme
                if latest_rsi > 70:
                    recommendation = "SAT"
                    recommendation_color = "red"
                elif latest_rsi < 30:
                    recommendation = "AL"
                    recommendation_color = "green"
                else:
                    recommendation = "BEKLE"
                    recommendation_color = "yellow"

                st.write(f"### Öneri: {recommendation}")

                # Gauge chart oluşturma
                fig_recommendation = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=latest_rsi,
                    title={"text": "RSI Önerisi"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'steps': [
                            {'range': [0, 30], 'color': "green"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': recommendation_color, 'width': 4},
                            'thickness': 0.75,
                            'value': latest_rsi
                        }
                    }
                ))

                fig_recommendation.update_layout(
                    paper_bgcolor="white",
                    font={'color': "black"}
                )

                st.plotly_chart(fig_recommendation)

            def plot_bollinger_bands(data, window=20):
                rolling_mean = data['Close'].rolling(window).mean()
                rolling_std = data['Close'].rolling(window).std()
                upper_band = rolling_mean + (rolling_std * 2)
                lower_band = rolling_mean - (rolling_std * 2)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
                fig.add_trace(go.Scatter(x=data.index, y=rolling_mean, mode='lines', name='Moving Average', line=dict(color='green')))
                fig.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band', line=dict(color='red')))
                fig.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band', line=dict(color='red')))
                fig.update_layout(shapes=[
                    dict(type='rect', xref='x', yref='y', x0=data.index[0], y0=lower_band.iloc[0], x1=data.index[-1], y1=upper_band.iloc[-1],
                         fillcolor='grey', opacity=0.1, layer='below', line_width=0)
                ])
                fig.update_layout(title='Bollinger Bands', xaxis_title='Date', yaxis_title='Price')
                st.plotly_chart(fig)

                # Bollinger Bandı gauge chart
                latest_close = data['Close'].iloc[-1]
                latest_upper_band = upper_band.iloc[-1]
                latest_lower_band = lower_band.iloc[-1]

                # Öneri belirleme
                if latest_close > latest_upper_band:
                    recommendation = "SAT"
                    recommendation_color = "red"
                elif latest_close < latest_lower_band:
                    recommendation = "AL"
                    recommendation_color = "green"
                else:
                    recommendation = "BEKLE"
                    recommendation_color = "yellow"

                st.write(f"### Öneri: {recommendation}")

                # Gauge chart oluşturma
                fig_recommendation = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=latest_close,
                    title={"text": "Bollinger Bandı Önerisi"},
                    gauge={
                        'axis': {'range': [latest_lower_band, latest_upper_band]},
                        'steps': [
                            {'range': [latest_lower_band, latest_close], 'color': "green" if latest_close < latest_lower_band else "yellow" if latest_close <= latest_upper_band else "red"}
                        ],
                        'threshold': {
                            'line': {'color': recommendation_color, 'width': 4},
                            'thickness': 0.75,
                            'value': latest_close
                        }
                    }
                ))

                fig_recommendation.update_layout(
                    paper_bgcolor="white",
                    font={'color': "black"}
                )

                st.plotly_chart(fig_recommendation)

            if indicator == "MACD":
                st.write("### MACD Grafiği")
                plot_macd(data)
            elif indicator == "RSI":
                st.write("### RSI Grafiği")
                plot_rsi(data)
            elif indicator == "BOLLINGER":
                st.write("### Bollinger Bantları Grafiği")
                plot_bollinger_bands(data)
            else:
                st.write("Veri alınamadı. Lütfen geçerli bir sembol seçin.")
