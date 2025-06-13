from openai import OpenAI
import streamlit as st
import matplotlib.pyplot as plt
from utils import get_stock_data, stocks
import os
from dotenv import load_dotenv

api_key = 'YOUR_API_KEY'

client = OpenAI(api_key=api_key)

def show_reporting():
    st.write("### Reporting")
    stock_name = st.selectbox("Select the stock you want to generate a report for:", list(stocks.keys()))
    
    if stock_name:
        symbol = stocks[stock_name]
        data = get_stock_data(symbol)
        
        if data is not None:
            average_price = data["Close"].mean()
            median_price = data["Close"].median()
            std_dev = data["Close"].std()
            min_price = data["Close"].min()
            max_price = data["Close"].max()

            # Decision Recommendations
            st.write("### Decision Recommendations")
            
            gpt_prompt = (
                f"You are performing stock analysis. Here are the key analysis results for {stock_name}:\n\n"
                f"- Average Price: {average_price}\n"
                f"- Median Price: {median_price}\n"
                f"- Standard Deviation: {std_dev}\n"
                f"- Minimum Price: {min_price}\n"
                f"- Maximum Price: {max_price}\n\n"
                f"Based on this information, should the user BUY or NOT BUY the stock {stock_name}? "
                f"Please explain your reasoning briefly. Only answer 'BUY' or 'DO NOT BUY'."
            )
            
            if st.button("Get GPT Recommendation"):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial analyst."},
                        {"role": "user", "content": gpt_prompt}
                    ],
                    max_tokens=500
                )
                
                st.write("### GPT Recommendation")
                response_message = response.choices[0].message.content
                st.write(response_message)

            # Visualizations
            st.write("### Visualizations")
            
            # Closing Price Time Series
            st.write("**Closing Price Time Series**")
            plt.figure(figsize=(10, 5))
            plt.plot(data['Close'], label='Closing Price')
            plt.title(f'{stock_name} Closing Price')
            plt.xlabel('Date')
            plt.ylabel('Closing Price')
            plt.legend()
            st.pyplot(plt)
            
            # Closing Price Histogram
            st.write("**Closing Price Histogram**")
            plt.figure(figsize=(10, 5))
            plt.hist(data['Close'], bins=50, alpha=0.7)
            plt.title(f'{stock_name} Closing Price Distribution')
            plt.xlabel('Closing Price')
            plt.ylabel('Frequency')
            st.pyplot(plt)
            
            # Closing Price Box Plot
            st.write("**Closing Price Box Plot**")
            plt.figure(figsize=(10, 5))
            plt.boxplot(data['Close'])
            plt.title(f'{stock_name} Closing Price Box Plot')
            plt.ylabel('Closing Price')
            st.pyplot(plt)

        else:
            st.write("Data could not be retrieved. Please select a valid stock symbol.")
