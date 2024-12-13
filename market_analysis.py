import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title(":green[Analyse des caractéristiques d'une voiture d'occasion] 🚗")
st.divider()

### PREMIER GRAPHE
df = pd.read_parquet("data_unique.parquet")

fig = px.bar(df["brand"].value_counts(), 
             x=df["brand"].value_counts().index, 
             y=df["brand"].value_counts().values, 
             labels={"x": "Marque", "y": "Nombre d'annonces"})

st.title("Répartition des marques")
st.plotly_chart(fig, use_container_width=True)

### DEUXIEME GRAPHE

df_heatmap = df.drop(["list_id", "url", "model", "brand", "fuel_type", "gearbox"], axis=1)
df_heatmap = df_heatmap.dropna()
df_heatmap['price_cents'] = df_heatmap['price_cents'] / 100

lower_quantile = 0.01
upper_quantile = 0.99

for col in df_heatmap.select_dtypes(include=['number']).columns:
    q_low = df_heatmap[col].quantile(lower_quantile)
    q_high = df_heatmap[col].quantile(upper_quantile)
    df_heatmap = df_heatmap[(df_heatmap[col] >= q_low) & (df_heatmap[col] <= q_high)]

# Calcul de la matrice de corrélation
correlation_matrix = df_heatmap.corr()

# Conversion des valeurs pour affichage (arrondi à 2 décimales)
text_values = correlation_matrix.round(2).astype(str).values

# Création de la heatmap avec Plotly
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale="YlGnBu",
    colorbar=dict(title="Corrélation"),
    text=text_values,  
    hoverinfo="text"   
))

fig.update_traces(
    texttemplate="%{text}",  
    textfont=dict(size=12),  
    showscale=True           
)

fig.update_layout(
    xaxis=dict(title="Variables", tickangle=-45),
    yaxis=dict(title="Variables"),
    autosize=True,
)

st.title("Matrice de corrélation")
st.plotly_chart(fig, use_container_width=True)

