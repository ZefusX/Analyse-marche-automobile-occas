import streamlit as st

st.title("Accueil")
st.markdown("##### Bienvenue sur mon site d'estimation et d'analyse du marché automobile !")
st.text("Vous souhaitez connaître la valeur de votre voiture ou comprendre les tendances du marché de l'occasion ? Vous êtes au bon endroit ! Grâce à notre outil d'estimation précis, obtenez rapidement le prix actuel de votre véhicule, basé sur des données réelles et actualisées. En plus, explorez nos analyses détaillées pour prendre des décisions éclairées, que vous soyez vendeur, acheteur ou simplement passionné par l'automobile.")
st.markdown(":green[Découvrez la valeur de votre voiture, suivez l'évolution du marché et trouvez les meilleures opportunités sur le marché de l'occasion. ]")

nav_price_estimation, nav_model_analysis, nav_market_analysis = st.columns(3)
with nav_price_estimation:
  if st.button("Estimation de prix"):
    st.navigation([st.Page("price_prediction.py")])
with nav_model_analysis:
  if st.button("Analyse d'un modèle", type="primary"):
    st.navigation([st.Page("model_analysis.py")])
with nav_market_analysis:
  if st.button("Analyse du marché"):
    st.navigation([st.Page("market_analysis.py")])