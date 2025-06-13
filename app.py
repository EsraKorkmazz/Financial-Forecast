import streamlit as st
from data_analysis import show_data_analysis
from arima_model import show_arima_model, linear_regression
from reporting import show_reporting

st.set_page_config(layout="wide") 

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f0; /* Change background color as you like */
    }
    </style>
    """,
    unsafe_allow_html=True)

def load_css():
    css = """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: white;  /* Background color */
            color: #000000;            /* Text color */
        }
        .css-18e3th9 {
            padding: 0px 16px;         /* Content padding */
        }
        .css-1d391kg {
            background-color: #005A5B; /* Sidebar background color */
            color: #FFFFFF;            /* Sidebar text color */
            font-size: 40px;           /* Font size */
            text-align: center;        /* Text alignment */
        }
        .st-bq {
            margin-bottom: 100px;      /* Spacing between menu options */
        }
        h1 {
            color: #3F8CCC;            /* Heading text color */
        }
        .css-1d391kg .css-bjfvzt {
            font-size: 50px;           /* Menu options font size */
            text-align: center;        /* Menu options text alignment */
        }
        .css-1d391kg .css-1v3fvcr {
            font-size: 60px;           /* Sidebar header font size */
            text-align: center;        /* Sidebar header alignment */
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #f0f0f0; /* Background color */
            color: #000000;            /* Text color */
        }
        
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_css()

st.title("Financial Data Analysis and Forecasting Application")
st.sidebar.header("Menu")
menu = st.sidebar.radio(
    "Options",
    ["Home", "Data Analysis", "Model Training and Forecasting", "Reporting"],
    format_func=lambda x: {
        "Home": "🏠 Home",
        "Data Analysis": "📊 Data Analysis",
        "Model Training and Forecasting": "🔍 Model Training and Forecasting",
        "Reporting": "📝 Reporting"
    }[x]
)

if menu == "Home":
    st.write("""
    ### Welcome!
    This application is developed for financial data analysis and forecasting. So, what is financial analysis? Financial analysis is a set of methods and processes used to evaluate the financial condition and performance of a company, sector, or project. These analyses are conducted using company financial statements, market trends, sector comparisons, and other relevant financial data. Financial analysis serves various purposes and is critical for businesses and investors.
    """)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(r"/Users/esra/Desktop/IST-DSA-PROJECTS/STOCK-PRICE/stock.jpg", caption="Financial Analysis Chart", width=500)
    st.write("""
    Financial analysis supports managers and decision-makers in making investment decisions, securing financing, allocating budgets, and other financial choices. Through these analyses, the financial health and market position of businesses are better understood. Financial analyses are used to evaluate a company's past performance and predict future performance. This helps identify areas that require improvement. Based on financial analysis results, companies can develop long-term business plans and strategies. These plans ensure sustainable growth and maintain competitive advantage. They also allow early identification of potential risks and issues, enabling companies to take precautions against possible financial crises.
    """)
    
elif menu == "Data Analysis":
    show_data_analysis()

elif menu == "Model Training and Forecasting":
    linear_regression()
    show_arima_model()

elif menu == "Reporting":
    show_reporting()
