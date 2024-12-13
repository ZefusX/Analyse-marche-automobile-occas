import streamlit as st

model_analysis_page = st.Page("model_analysis.py", title="Analyse d'un modèle", icon=":material/trending_up:")
price_prediction_page = st.Page("price_prediction.py", title="Estimateur de prix", icon=":material/request_quote:")
market_analysis_page = st.Page("market_analysis.py", title="Analyse du marché", icon=":material/monitoring:")
home_page = st.Page("home.py", title="Accueil", icon=":material/home:")



pg = st.navigation({"Navigation": [home_page, model_analysis_page, price_prediction_page, market_analysis_page]})
pg.run()