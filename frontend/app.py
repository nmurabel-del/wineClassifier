import requests
import streamlit as st
# ==========================================================
# CONFIGURATION
# ==========================================================
API_URL = "http://localhost:8000/predict"
TIMEOUT = 10
st.set_page_config(
    page_title="Wine Intelligence",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================================================
# STYLE CSS
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root {
    --wine: #591B2B;
    --wine-dark: #35101D;
    --gold: #B58A45;
    --cream: #F7F4EE;
    --white: #FFFFFF;
    --text: #30252A;
    --muted: #82777A;
}
.stApp {
    background-color: var(--cream);
    font-family: 'DM Sans', sans-serif;
}
header {
    visibility: visible;
}
.main .block-container {
    max-width: 1250px;
    padding: 2rem 3rem 3rem 3rem;
}
[data-testid="stSidebar"] {
    background-color: var(--wine-dark);
}
[data-testid="stSidebar"] * {
    color: white;
}
.sidebar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 27px;
    color: #E5C58E;
    font-weight: bold;
    padding: 20px 0;
}
.sidebar-caption {
    color: #D0B9B9;
    font-size: 13px;
    line-height: 1.7;
}
.hero {
    background: linear-gradient(120deg, #35101D, #702B40);
    padding: 42px;
    border-radius: 20px;
    margin-bottom: 30px;
    color: white;
    position: relative;
}
.hero-label {
    color: #E5C58E;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 43px;
    color: #FFFFFF;
    margin: 15px 0;
}
.hero p {
    color: #E8D9D9;
    font-size: 15px;
    line-height: 1.8;
    max-width: 700px;
}
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    color: var(--wine-dark);
    margin: 25px 0 8px 0;
}
.section-description {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 20px;
}
.metric-card {
    background: white;
    padding: 23px;
    border-radius: 14px;
    border: 1px solid #EAE3DB;
    min-height: 115px;
}
.metric-title {
    color: #82777A;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.metric-value {
    color: var(--wine);
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    font-weight: bold;
    margin-top: 10px;
}
.stNumberInput label {
    color: var(--wine-dark) !important;
    font-weight: 600 !important;
}
.stNumberInput input {
    border-radius: 9px !important;
}
div.stButton > button {
    background: var(--wine);
    color: white;
    border: none;
    border-radius: 10px;
    height: 52px;
    font-weight: 700;
    font-size: 15px;
    transition: 0.3s;
}
div.stButton > button:hover {
    background: var(--wine-dark);
    color: #E5C58E;
    border: 1px solid var(--gold);
}
.result-card {
    background: white;
    border: 1px solid #E7DCCB;
    border-left: 6px solid var(--gold);
    border-radius: 15px;
    padding: 30px;
    margin-top: 25px;
}
.result-label {
    color: var(--muted);
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 2px;
}
.result-class {
    color: var(--wine);
    font-family: 'Playfair Display', serif;
    font-size: 35px;
    font-weight: bold;
    margin-top: 10px;
}
.footer {
    text-align: center;
    color: #92868A;
    font-size: 12px;
    padding: 35px 0 10px 0;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 15px;
    border: 1px solid #EAE3DB;
}
.stApp {
    color: #000000 !important;
}
:where(.stMarkdown) p,
:where(.stMarkdown) li {
    color: #000000;
}

/* Bouton, y compris celui du formulaire */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: var(--wine) !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    height: 52px;
    font-weight: 700;
}
div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--wine-dark) !important;
    color: #E5C58E !important;
    border: 1px solid var(--gold);
}
div.stButton > button p,
div[data-testid="stFormSubmitButton"] > button p {
    c
</style>
""", unsafe_allow_html=True)
# ==========================================================
# DONNEES DU WINE DATASET
# ==========================================================
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
    ("od280_od315_of_diluted_wines", "OD280 / OD315", 2.61),
    ("proline", "Proline", 746.9)
]
# ==========================================================
# BARRE LATERALE
# ==========================================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">🍷 Wine Intelligence</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-caption">'
        'Plateforme intelligente de classification '
        'des vins par Machine Learning.'
        '</div>',
        unsafe_allow_html=True
    )
    st.divider()
    page = st.radio(
        "NAVIGATION",
        ["Accueil", "Classification", "À propos"]
    )
# ==========================================================
# PAGE ACCUEIL
# ==========================================================
if page == "Accueil":
    st.markdown("""
    <div class="hero">
        <div class="hero-label">MACHINE LEARNING · DATA SCIENCE</div>
        <h1>Wine Intelligence</h1>
        <p>
            Découvrez une nouvelle approche de la classification
            des vins grâce à l'intelligence artificielle.
            Notre système exploite les caractéristiques chimiques
            pour prédire automatiquement la classe d'un vin.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="section-heading">Notre plateforme</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">'
        'Un outil de classification basé sur les données chimiques du vin.'
        '</div>',
        unsafe_allow_html=True
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Variables</div>
            <div class="metric-value">13 caractéristiques</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Technologie</div>
            <div class="metric-value">Machine Learning</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Classification</div>
            <div class="metric-value">3 classes</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "Pour commencer, rendez-vous dans la rubrique "
        "'Classification' située dans le menu latéral."
    )
# ==========================================================
# PAGE CLASSIFICATION
# ==========================================================
elif page == "Classification":
    st.markdown("""
    <div class="hero">
        <div class="hero-label">ANALYSE DES DONNEES</div>
        <h1>Classification du vin</h1>
        <p>
            Renseignez les caractéristiques chimiques de votre échantillon.
            Notre modèle analysera les données et proposera une classe.
        </p>
    </div>
    """, unsafe_allow_html=True)
    values = {}
    st.markdown(
        '<div class="section-heading">01 — Caractéristiques chimiques</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">'
        'Remplissez les champs ci-dessous pour décrire votre échantillon.'
        '</div>',
        unsafe_allow_html=True
    )
    # Organisation en trois catégories visuelles
    sections = [
        ("Composition générale", FEATURES[0:5]),
        ("Composés phénoliques", FEATURES[5:9]),
        ("Caractéristiques complémentaires", FEATURES[9:13])
    ]
    with st.form("wine_form"):
        for section_name, section_features in sections:
            st.markdown(f"*{section_name}*")
            columns = st.columns(2)
            for i, (name, label, default) in enumerate(section_features):
                with columns[i % 2]:
                    values[name] = st.number_input(
                        label,
                        min_value=0.0,
                        value=float(default),
                        format="%.2f",
                        key=name
                    )
            st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "Prédire",
            use_container_width=True
        )
    # ======================================================
    # ENVOI A L'API
    # ======================================================
    if submitted:
        with st.spinner("Analyse en cours..."):
            try:
                response = requests.post(
                    API_URL,
                    json=values,
                    timeout=TIMEOUT
                )
                response.raise_for_status()
                result = response.json()
                prediction = result.get(
                    "prediction",
                    result.get("class")
                )
                if prediction is None:
                    st.warning(
                        f"Réponse inattendue de l'API : {result}"
                    )
                else:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-label">
                            Résultat de la prédiction
                        </div>
                        <div class="result-class">
                            Classe {prediction}
                        </div>
                        <p>
                            La classification de votre échantillon
                            a été effectuée avec succès.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.error(
                    "Connexion impossible. Vérifiez que l'API "
                    "FastAPI est démarrée et que son adresse est correcte."
                )
            except requests.exceptions.Timeout:
                st.error("Le serveur met trop de temps à répondre.")
            except requests.exceptions.HTTPError as e:
                st.error(f"Erreur HTTP : {e}")
            except ValueError:
                st.error("La réponse reçue n'est pas un JSON valide.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de communication : {e}")
# ==========================================================
# PAGE A PROPOS
# ==========================================================
elif page == "À propos":
    st.markdown("""
    <div class="hero">
        <div class="hero-label">A PROPOS DU PROJET</div>
        <h1>Wine Intelligence</h1>
        <p>
            Un projet académique mettant en œuvre les techniques
            de classification supervisée pour analyser les
            caractéristiques chimiques des vins.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="section-heading">Objectif du système</div>',
        unsafe_allow_html=True
    )
    st.write(
        "Le système permet de prédire la classe d'un vin "
        "à partir de treize caractéristiques chimiques."
    )
    st.markdown(
        '<div class="section-heading">Technologies utilisées</div>',
        unsafe_allow_html=True
    )
    st.write("""
    - Python : langage de programmation.
    - Streamlit : création de l'interface utilisateur.
    - FastAPI : communication avec le modèle.
    - Scikit-learn : entraînement du modèle de classification.
    - Joblib : sauvegarde et chargement du modèle.
    """)
# ==========================================================
# PIED DE PAGE
# ==========================================================
st.markdown("""
<div class="footer">
    WINE INTELLIGENCE · PROJET DATA SCIENCE
    <br>
    Classification intelligente des vins
</div>
""", unsafe_allow_html=True)