import streamlit as st
from data_analysis import show_data_analysis
from arima_model import show_arima_model, linear_regression
from reporting import show_reporting

st.set_page_config(layout="wide")  # Sayfa genişliğini tam genişlik olarak ayarlar

# Yan panel için stil
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f0; /* Arka plan rengini istediğiniz renk koduna değiştirin */
    }
    </style>
    """,
    unsafe_allow_html=True)

def load_css():
    css = """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: white;  /* Arka plan rengi */
            color: #000000;            /* Metin rengi */
        }
        .css-18e3th9 {
            padding: 0px 16px;         /* İçerik padding ayarı */
        }
        .css-1d391kg {
            background-color: #005A5B; /* Sidebar arka plan rengi */
            color: #FFFFFF;            /* Sidebar metin rengi */
            font-size: 40px;           /* Font boyutu */
            text-align: center;        /* Metin ortalama */
        }
        .st-bq {
            margin-bottom: 100px;       /* Menü seçenekleri arası boşluk */
        }
        h1 {
            color: #3F8CCC;            /* Başlık metin rengi */
        }
        .css-1d391kg .css-bjfvzt {
            font-size: 50px;           /* Menü seçenekleri yazı boyutu */
            text-align: center;        /* Menü seçenekleri ortalama */
        }
        .css-1d391kg .css-1v3fvcr {
            font-size: 60px;           /* Sidebar başlık yazı boyutu */
            text-align: center;        /* Sidebar başlık ortalama */
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #f0f0f0; /* Arka plan rengi */
            color: #000000; /* Metin rengi */
        }
        
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# CSS'i yükle
load_css()

st.title("Finansal Veri Analizi ve Tahminleme Uygulaması")
st.sidebar.header("Menü")
menu = st.sidebar.radio(
    "Seçenekler",
    ["Ana Sayfa", "Veri Analizi", "Model Eğitimi ve Tahminleme", "Raporlama"],
    format_func=lambda x: {"Ana Sayfa": "🏠 Ana Sayfa", "Veri Analizi": "📊 Veri Analizi", "Model Eğitimi ve Tahminleme": "🔍 Model Eğitimi ve Tahminleme", "Raporlama": "📝 Raporlama"}[x]
)

if menu == "Ana Sayfa":
    st.write("""
    ### Hoşgeldiniz!
    Bu uygulama finansal veri analizi ve tahminleme işlemleri için geliştirilmiştir. Peki finansal analiz nedir? Finansal analiz, bir şirketin, sektörün ya da projenin finansal durumunu ve performansını değerlendirmek için kullanılan bir dizi yöntem ve süreçtir. Bu analizler, şirketlerin mali tabloları, piyasa trendleri, sektör karşılaştırmaları ve diğer ilgili finansal verileri kullanarak yapılır. Finansal analiz, çeşitli amaçlar için yapılır ve işletmeler ile yatırımcılar için kritik öneme sahiptir.
    """)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(r"/Users/esra/Desktop/IST-DSA-PROJECTS/STOCK-PRICE/stock.jpg", caption="Finansal Analiz Grafiği", width=500)
    st.write("""
    Finansal analiz, yöneticilere ve karar vericilere, yatırım yapma, finansman sağlama, bütçe ayırma ve diğer mali kararları verme konusunda destek olur. Bu analizler sayesinde, işletmelerin finansal sağlığı ve pazar konumu daha iyi anlaşılır. Şirketlerin geçmiş performansını değerlendirmek ve gelecekteki performansı öngörmek için finansal analizler kullanılır. Bu sayede şirketlerin hangi alanlarda iyileştirme yapması gerektiği belirlenebilir. Şirketler, finansal analiz sonuçlarına dayanarak uzun vadeli iş planları ve stratejiler geliştirebilir. Bu planlar, şirketin sürdürülebilir büyümesini ve rekabet avantajını korumasını sağlar. Potansiyel riskleri ve sorunları önceden belirleme imkanı sağlar. Bu sayede şirketler, olası mali krizlere karşı önlem alabilir.
    """)
elif menu == "Veri Analizi":
    show_data_analysis()

elif menu == "Model Eğitimi ve Tahminleme":
    linear_regression()
    show_arima_model()

elif menu == "Raporlama":
    show_reporting()
    
