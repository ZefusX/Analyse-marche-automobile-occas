import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def price_f_mileage(df, brand, model):
    # Filtrer les données pour la marque et le modèle spécifiés
    df = df[(df['brand'] == brand) & (df['model'] == model)]

    # Supprimer les valeurs aberrantes
    lower_quantile = 0.01
    upper_quantile = 0.99
    q_low = df["price_cents"].quantile(lower_quantile)
    q_high = df["price_cents"].quantile(upper_quantile)
    df = df[(df["price_cents"] >= q_low) & (df["price_cents"] <= q_high)]
    
    q_low = df["mileage"].quantile(lower_quantile)
    q_high = df["mileage"].quantile(upper_quantile)
    df = df[(df["mileage"] >= q_low) & (df["mileage"] <= q_high)]

    # Prix en €
    df["price_cents"] = df["price_cents"] / 100

    # Ajustement polynomiale de degré 2
    coeffs = np.polyfit(df['mileage'], df['price_cents'], 2)
    poly = np.poly1d(coeffs)

    # Génération valeurs courbe de tendance
    x = np.linspace(df['mileage'].min(), df['mileage'].max(), 100)
    y = poly(x)

    fig = go.Figure()

    # Ajouter les données sous forme de nuage de points
    fig.add_trace(go.Scatter(
        x=df['mileage'],
        y=df['price_cents'],
        mode='markers',
        name='Données',
        marker=dict(color='skyblue', size=6, opacity=0.7)
    ))

    # Ajouter la courbe de tendance polynomiale
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Tendance (polynôme degré 2)',
        line=dict(color='red', width=2)
    ))

    # Mise en forme du graphique
    fig.update_layout(
        title="Prix en fonction du Kilométrage avec courbe de tendance polynomiale",
        xaxis_title="Kilométrage",
        yaxis_title="Prix (€)",
        template="plotly_dark",
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        autosize=True,
        
    )

    # Retourner l'objet Figure
    return fig
  
   
st.title(":green[Analyse des caractéristiques d'une voiture d'occasion] 🚗")
st.divider()

df = pd.read_parquet("data_unique.parquet")

brands = df["brand"].dropna().unique()
models = df["model"].dropna().unique()
years = df["year"].dropna().unique()


input_brand, input_model, input_year = st.columns(3)
with input_brand:
    marque = st.selectbox("Sélectionnez la marque :", options=[""] + sorted(brands))
with input_model:
    modele = st.selectbox("Sélectionnez le modèle :", options=[""] + sorted(models))
with input_year:
    annee = st.selectbox("Sélectionnez l'année (optionnel) :", options=[""] + sorted(years))

st.divider()


if marque and modele:
    results = df[(df["brand"].str.contains(marque, case=False)) &
                 (df["model"].str.contains(modele, case=False))]
    if annee:
        results = results[results["year"] == int(annee)]

    st.title("Résultats :")
    #st.dataframe(results)
    avg, med, mile = st.columns(3)
    with avg:
        st.markdown("### Prix moyen :")
        st.markdown(f"##### :green[**{round(results['price_cents'].mean()/100, 2)}€**]")
    with med:
        st.markdown("### Prix médian :")
        st.markdown(f"##### :green[**{results['price_cents'].median()/100}€**]")
    with mile:
        st.markdown("### Km moyen :")
        st.markdown(f"##### :green[**{round(results['mileage'].mean())}km**]")
    st.markdown(f"###### :grey[Nombre de données : {results.shape[0]}]")
      
    st.divider()
    
    plot_price_vs_mileage = price_f_mileage(df, marque, modele)
    st.plotly_chart(plot_price_vs_mileage)

else:
    st.write("Entrez une marque et un modèle pour rechercher.")