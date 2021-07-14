# from: https://github.com/upraneelnihar/streamlit-multiapps
#app.py
import streamlit as st
from multiapp import MultiApp
from apps import home, stock_summary, sentiment     # import your app modules here

st.set_page_config(
    # page_title="hvFinance",
    # page_icon="chart_with_upwards_trend",
    layout="wide",
)

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Stock Analysis", stock_summary.app)
app.add_app("Market Sentiment", sentiment.app)


# The main app
app.run()

