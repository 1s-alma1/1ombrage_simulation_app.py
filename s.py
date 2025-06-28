import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURATION
st.set_page_config(page_title="Simulation Photovoltaïque ☀️", layout="centered")
st.title("☀️ Simulation d’un Système Photovoltaïque Résidentiel")
st.markdown("Simulez la production, le rendement et l’injection selon vos choix de panneaux, météo, ville et nombre de panneaux.")

# CHOIX DE LA VILLE
ville = st.selectbox(
    " Choisissez la ville",
    ["Marseille", "Lyon", "Toulouse", "Bordeaux", "Nantes",
     "Paris", "Strasbourg", "Lille", "Metz", "Colmar", "Nice", "Montpellier"]
)

# IRRADIATION ANNUELLE PAR VILLE (kWh/m²/an)
irradiation_par_ville = {
    "Marseille": 1824,
    "Lyon": 1470,
    "Toulouse": 1610,
    "Bordeaux": 1575,
    "Nantes": 1420,
    "Paris": 1340,
    "Strasbourg": 1300,
    "Lille": 1190,
    "Metz": 1220,
    "Colmar": 1280,
    "Nice": 1800,
    "Montpellier": 1790
}

irradiation_ville = irradiation_par_ville[ville]

# ENTRÉES UTILISATEUR
panneau = st.selectbox(" Type de panneau solaire", ["Monocristallin", "Polycristallin", "Amorphe", "Hétérojonction", "Bifacial"])
meteo = st.radio("🌦️ Conditions météorologiques", ["Ensoleillé", "Nuageux", "Pluvieux"])
nb_panneaux = st.slider(" Nombre de panneaux", 0, 25, 20)

# DONNÉES DE BASE
surface_par_module = 1.7  # m²
surface_totale = nb_panneaux * surface_par_module
puissance_par_panneau = 0.4  # kWc
puissance_kWp = nb_panneaux * puissance_par_panneau
puissance_kWp_ref = 8  # Référence sur 20 panneaux mono 400 Wc

# FACTEURS MÉTÉO
facteur_meteo = {"Ensoleillé": 1.0, "Nuageux": 0.75, "Pluvieux": 0.55}[meteo]
emoji_meteo = {"Ensoleillé": "☀️", "Nuageux": "☁️", "Pluvieux": "🌧️"}[meteo]

# DONNÉES TECHNIQUES DES PANNEAUX
data = {
    "Monocristallin": {"rendement": 20.0, "prix": 1.20, "prod_ref": 11862},
    "Polycristallin": {"rendement": 17.5, "prix": 1.00, "prod_ref": 10500},
    "Amorphe": {"rendement": 10.0, "prix": 0.80, "prod_ref": 6000},
    "Hétérojonction": {"rendement": 21.5, "prix": 1.50, "prod_ref": 12500},
    "Bifacial": {"rendement": 19.5, "prix": 1.40, "prod_ref": 11200}
}

# CALCULS ADAPTÉS À LA VILLE
rendement = data[panneau]["rendement"]
prod_ref_marseille = data[panneau]["prod_ref"]
irradiation_ref = 1824  # Base Marseille
prod_ref = prod_ref_marseille * (irradiation_ville / irradiation_ref)
prix_watt = data[panneau]["prix"]

production = (puissance_kWp / puissance_kWp_ref) * prod_ref * facteur_meteo
efficacite = production / surface_totale if surface_totale else 0
cout_total = puissance_kWp * 1000 * prix_watt

# HYPOTHÈSE CONSOMMATION BÂTIMENT
conso_batiment = 8260  # kWh/an
autoconso = min(conso_batiment, production) * 0.9
injecte = max(0, production - autoconso)
reprise = max(0, conso_batiment - autoconso)

# AFFICHAGE DES RÉSULTATS
st.subheader(f"{emoji_meteo} Résultats de simulation")
st.markdown(f" **Ville sélectionnée : `{ville}` – Irradiation : `{irradiation_ville} kWh/m²/an`**")

col1, col2 = st.columns(2)
col1.metric("Production estimée", f"{production:.0f} kWh/an")
col2.metric("Puissance installée", f"{puissance_kWp:.2f} kWc")

col1, col2 = st.columns(2)
col1.metric("Production par surface", f"{efficacite:.1f} kWh/m²/an")
col2.metric("Coût estimé panneaux", f"{cout_total:,.0f} €")

st.markdown(f" **Rendement du panneau _{panneau}_ : `{rendement:.1f}%`**")

# GRAPHIQUE RÉPARTITION ÉNERGIE
st.subheader(" Répartition de l’énergie")

fig1, ax1 = plt.subplots()
labels = ["Autoconsommée", "Injectée au réseau", "Reprise réseau"]
values = [autoconso, injecte, reprise]
colors = ["green", "orange", "red"]
ax1.bar(labels, values, color=colors)
ax1.set_ylabel("Énergie (kWh)")
ax1.set_title("Répartition annuelle de l'énergie")
ax1.grid(axis='y')
st.pyplot(fig1)

# SIGNATURE
st.markdown("---")
st.markdown("👩‍🎓 **Attaibe Salma – Université de Lorraine**")
st.caption("Simulation fondée sur PVsyst, projet S8 – Juin 2025")
