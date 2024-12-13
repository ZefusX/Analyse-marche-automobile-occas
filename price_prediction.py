import warnings

import joblib
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')

# Charger les données depuis un fichier Parquet
def charger_donnees_parquet(fichier_parquet):
    return pd.read_parquet(fichier_parquet)

def entrainer_modele_prix(data):
    # Supprimer les lignes contenant des valeurs manquantes
    data = data.dropna()

    # Séparer les features (X) et la cible (y)
    X = data.drop(columns=['price_cents'])
    y = data['price_cents']
    
    # Appliquer get_dummies pour gérer les variables catégorielles avant la séparation des données
    X = pd.get_dummies(X, columns=['brand',"model"], drop_first=True)
    
    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Entraîner le modèle RandomForestRegressor
    forest = RandomForestRegressor()
    forest.fit(X_train, y_train)
    print(forest.score(X_test, y_test))
    
    # Sauvegarder le modèle
    joblib.dump(forest, 'modele_prix.pkl', compress=("gzip", 3))
    return forest

def charger_modele():
    # Charger le modèle préalablement entraîné
    return joblib.load('modele_prix.pkl')

def estimer_prix(modele, model, brand, year, horsepower, mileage, nb_doors, nb_seats, gearbox, f_horsepower, fuel_type):
    # Créer un DataFrame pour une seule observation
    data = pd.DataFrame([{
        'brand': brand,
        'model': model,
        'year': year,
        'horsepower': horsepower,
        'mileage': mileage,
        'nb_doors': nb_doors,
        'nb_seats': nb_seats,
        'gearbox': gearbox,
        'f_horsepower': f_horsepower,
        'fuel_type': fuel_type
    }])
    
    # Appliquer get_dummies sur les nouvelles données, comme pour l'entraînement
    data = pd.get_dummies(data, columns=['brand', 'model'], drop_first=True)
    
    # Ajouter les colonnes manquantes si nécessaire (par exemple, "brand_Renault" s'il manque)
    missing_cols = set(modele.feature_names_in_) - set(data.columns)
    
    # Créer un dictionnaire avec les colonnes manquantes initialisées à 0
    for col in missing_cols:
        data[col] = 0
    
    # Réordonner les colonnes pour correspondre à l'ordre des colonnes d'entraînement
    data = data[modele.feature_names_in_]
    
    # Prédire le prix
    price_cents = modele.predict(data)[0]
    return price_cents

# Charger les données
data = charger_donnees_parquet("data_unique.parquet")

# Nettoyage des données (enlever des colonnes inutiles et remplacer les valeurs de carburant)
data = data.drop(columns=["url", "list_id"])
data['fuel_type'] = data['fuel_type'].replace({'Essence': 1, 'Diesel': 2})

# Entraîner ou charger le modèle
try:
    modele_prix = charger_modele()
except FileNotFoundError:
    modele_prix = entrainer_modele_prix(data)

# Interface Streamlit
st.title(":green[Prédiction du prix d'une voiture] 🚗")
st.divider()
st.text("Beta ⚠️")
df = pd.read_parquet("data_unique.parquet")

brands = df["brand"].dropna().unique()
models = df["model"].dropna().unique()

input_brand, input_model, input_year = st.columns(3)
input_hpf, input_mileage, input_doors = st.columns(3)
input_seats, input_hp, input_gearbox, input_fuel_type = st.columns(4)

with input_brand:
  marque = st.selectbox("Sélectionnez la marque :", options=[""] + sorted(brands))
with input_model:
  modele = st.selectbox("Sélectionnez le modèle :", options=[""] + sorted(models))
with input_year:
  annee = st.number_input("Entrez l'année")
with input_hpf:
  hpf = st.number_input("Entrez le nombre de cv fiscaux :")
with input_mileage:
  mileage = st.number_input("Entrez le kilométrage :")
with input_doors:
  doors = st.number_input("Entrez le nombre de portes :")
with input_seats:
  seats = st.number_input("Entrez le nombre de places :")
with input_hp:
  hp = st.number_input("Entrez le nombre de chevaux :")
with input_gearbox:
  gearbox = st.selectbox("Sélectionner le type de boîte de vitesse :", options=[1,0])
with input_fuel_type:
  fuel_type = st.selectbox("Sélectionner le type de carburant", options=[1,0])

st.divider()
send_button = st.button("Estimer")
if send_button:
  with st.spinner('Chargement (peut prendre plusieurs dizaines de secondes)'):
    print(modele, marque, annee, hpf, mileage, doors, seats, gearbox, hp, fuel_type)
    prix_estime = estimer_prix(
      modele_prix, 
      model=modele, 
      brand=marque, 
      year=annee, 
      horsepower=hpf, 
      mileage=mileage, 
      nb_doors=doors, 
      nb_seats=seats, 
      gearbox=gearbox, 
      f_horsepower=hp, 
      fuel_type=fuel_type
    )
  st.divider()
  st.toast("Chargement fini !", icon="✔️")
  st.balloons()
  st.title(":red[Prix estimé : ]")
  st.success(f"Résultat : {prix_estime/100}€")
