import streamlit as st
import pandas as pd
from utils import get_stock_data, stocks, plot_moving_average
import plotly.graph_objs as go

def show_data_analysis():
    st.write("### Data Analysis")
    stock_name = st.selectbox("Please select the stock you want to analyze:", list(stocks.keys()))
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        if data is not None:
            st.write("### Loaded Data")
            
            # Highlight maximum values in columns
            def highlight_max(s):
                '''
                Highlight rows based on the maximum value in the column
                '''
                is_max = s == s.max()
                return ['background-color: red' if v else '' for v in is_max]
            
            # Sorting and filtering data
            # Filter applied: only rows where Close price is above 105, sorted by date descending
            sorted_data = data.sort_values(by='Date', ascending=False)
            filtered_data = sorted_data[sorted_data['Close'] > 105]
            styled_data = filtered_data.style.apply(highlight_max, subset=['Open', 'Close', 'Volume'], axis=0)
            st.dataframe(styled_data)

            st.write("### Data Statistics")
            st.write(data.describe())

            st.write("### Time Series Chart")
            fig_close = go.Figure()
            fig_close.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
            st.plotly_chart(fig_close)

            st.write("### Volume Chart")
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'))
            st.plotly_chart(fig_volume)
            
            st.write("### Moving Average Calculation")
            window = st.slider("Moving Average Window (Days)", min_value=1, max_value=50, value=20)
            plot_moving_average(data, window)
            
            st.write("### Indicator Selection")
            indicator = st.selectbox("Please select the indicator you want to analyze:", ["MACD", "RSI", "BOLLINGER"])
            
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
                    title={'text': "MACD Value"},
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
                
                # Buy/Sell recommendation
                if latest_macd > latest_signal:
                    recommendation = "BUY"
                    recommendation_color = "green"
                else:
                    recommendation = "SELL"
                    recommendation_color = "red"

                st.write(f"### Recommendation: {recommendation}")

                fig_recommendation = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=latest_macd,
                    number={'prefix': f"{recommendation} - "},
                    delta={'position': "top", 'reference': latest_signal},
                    title={"text": "Buy/Sell Signal"},
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

                # Recommendation logic
                if latest_rsi > 70:
                    recommendation = "SELL"
                    recommendation_color = "red"
                elif latest_rsi < 30:
                    recommendation = "BUY"
                    recommendation_color = "green"
                else:
                    recommendation = "HOLD"
                    recommendation_color = "yellow"

                st.write(f"### Recommendation: {recommendation}")

                fig_recommendation = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=latest_rsi,
                    title={"text": "RSI Recommendation"},
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

                # Bollinger Bands gauge chart
                latest_close = data['Close'].iloc[-1]
                latest_upper_band = upper_band.iloc[-1]
                latest_lower_band = lower_band.iloc[-1]

                # Recommendation logic
                if latest_close > latest_upper_band:
                    recommendation = "SELL"
                    recommendation_color = "red"
                elif latest_close < latest_lower_band:
                    recommendation = "BUY"
                    recommendation_color = "green"
                else:
                    recommendation = "HOLD"
                    recommendation_color = "yellow"

                st.write(f"### Recommendation: {recommendation}")

                fig_recommendation = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=latest_close,
                    title={"text": "Bollinger Bands Recommendation"},
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
                st.write("### MACD Chart")
                plot_macd(data)
            elif indicator == "RSI":
                st.write("### RSI Chart")
                plot_rsi(data)
            elif indicator == "BOLLINGER":
                st.write("### Bollinger Bands Chart")
                plot_bollinger_bands(data)
        else:
            st.write("Data not available. Please select a valid symbol.")
