"""
Wine Classifier - Interface utilisateur (Équipe 2)
Lancer avec : streamlit run frontend/app.py
"""

import requests
import streamlit as st

# ------------------------------------------------------------------
# Configuration : à ajuster avec l'équipe 3 (adresse de l'API)
# ------------------------------------------------------------------
API_URL = "http://localhost:8000/predict"
TIMEOUT = 10  # secondes

# Les 13 caractéristiques, dans le même ordre que le Wine Dataset.
# Format : (nom envoyé à l'API, libellé affiché, valeur par défaut)
# ATTENTION : les noms doivent être identiques à ceux de l'API (équipe 3).
FEATURES = [
    ("alcohol", "Alcool", 13.0),
    ("malic_acid", "Acide malique", 2.34),
    ("ash", "Cendres", 2.37),
    ("alcalinity_of_ash", "Alcalinité des cendres", 19.5),
    ("magnesium", "Magnésium", 99.7),
    ("total_phenols", "Phénols totaux", 2.30),
    ("flavanoids", "Flavonoïdes", 2.03),
    ("nonflavanoid_phenols", "Phénols non flavonoïdes", 0.36),
    ("proanthocyanins", "Proanthocyanidines", 1.59),
    ("color_intensity", "Intensité de la couleur", 5.06),
    ("hue", "Teinte", 0.96),
    ("od280_od315_of_diluted_wines", "OD280/OD315 des vins dilués", 2.61),
    ("proline", "Proline", 746.9),
]

# ------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------
st.set_page_config(page_title="Wine Classifier", page_icon="🍷")
st.title("🍷 Wine Classifier")
st.write("Saisissez les 13 caractéristiques du vin, puis cliquez sur *Prédire*.")

values = {}
col1, col2 = st.columns(2)
for i, (name, label, default) in enumerate(FEATURES):
    column = col1 if i % 2 == 0 else col2
    with column:
        values[name] = st.number_input(
            label, min_value=0.0, value=float(default), format="%.2f", key=name
        )

if st.button("Prédire", type="primary"):
    try:
        response = requests.post(API_URL, json=values, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()

        # Le nom de la clé dépend de l'API (équipe 3) : adapter si besoin
        prediction = result.get("prediction", result.get("class"))
        if prediction is None:
            st.warning(f"Réponse inattendue de l'API : {result}")
        else:
            st.success(f"Classe prédite : *{prediction}*")

    except requests.exceptions.ConnectionError:
        st.error(
            "Impossible de se connecter à l'API. "
            f"Vérifiez qu'elle est lancée et que l'adresse est correcte ({API_URL})."
        )
    except requests.exceptions.Timeout:
        st.error("L'API met trop de temps à répondre. Réessayez dans un instant.")
    except requests.exceptions.HTTPError as e:
        st.error(f"L'API a renvoyé une erreur : {e}")
    except ValueError:
        st.error("La réponse de l'API n'est pas un JSON valide.")