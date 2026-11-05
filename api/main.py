from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field


# --------------------------------------------------
# 1. CHEMIN DU MODÈLE
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "wine_model.joblib"


# --------------------------------------------------
# 2. LES 13 CARACTÉRISTIQUES DU VIN
# --------------------------------------------------

class WineFeatures(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float = Field(
        alias="od280/od315_of_diluted_wines"
    )
    proline: float


# --------------------------------------------------
# 3. CHARGEMENT DU MODÈLE
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Modèle introuvable : {MODEL_PATH}"
        )

    artifact = joblib.load(MODEL_PATH)

    # Les 13 caractéristiques utilisées pendant l'entraînement
    default_features = [
        "alcohol",
        "malic_acid",
        "ash",
        "alcalinity_of_ash",
        "magnesium",
        "total_phenols",
        "flavanoids",
        "nonflavanoid_phenols",
        "proanthocyanins",
        "color_intensity",
        "hue",
        "od280/od315_of_diluted_wines",
        "proline"
    ]

    # Accepter les deux formats de sauvegarde
    if isinstance(artifact, dict) and "model" in artifact:

        app.state.model = artifact["model"]
        app.state.feature_names = artifact.get(
            "feature_names", default_features
        )
        app.state.target_names = artifact.get("target_names")

    else:
        # Ton train.py sauvegarde directement le Pipeline
        app.state.model = artifact

        app.state.feature_names = list(
            getattr(artifact, "feature_names_in_", default_features)
        )

        app.state.target_names = None

    print("Modèle chargé avec succès !")
    print("Caractéristiques :", app.state.feature_names)

    yield

# --------------------------------------------------
# 4. CRÉATION DE L'API
# --------------------------------------------------

app = FastAPI(
    title="Wine Classifier API",
    description="API de prédiction de la classe d'un vin",
    version="1.0.0",
    lifespan=lifespan
)


# Autoriser la communication avec Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 5. ROUTE D'ACCUEIL
# --------------------------------------------------

@app.get("/")
def accueil():
    return {
        "message": "Bienvenue sur l'API Wine Classifier",
        "documentation": "/docs",
        "route_prediction": "/predict"
    }


# --------------------------------------------------
# 6. VÉRIFIER QUE L'API ET LE MODÈLE FONCTIONNENT
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "OK",
        "model_loaded": hasattr(app.state, "model")
    }


# --------------------------------------------------
# 7. ROUTE DE PRÉDICTION
# --------------------------------------------------

@app.post("/predict")
def predict_wine(wine: WineFeatures):

    try:
        # Récupérer les 13 valeurs avec les noms exacts
        # attendus par le modèle.
        wine_data = wine.model_dump(by_alias=True)

        # Respecter exactement l'ordre des colonnes utilisé
        # pendant l'entraînement du modèle.
        input_data = pd.DataFrame(
            [[wine_data[name] for name in app.state.feature_names]],
            columns=app.state.feature_names
        )

        # Effectuer la prédiction
        prediction = app.state.model.predict(input_data)[0]

        predicted_class = int(prediction)

        # Transformer le numéro en nom de classe
        target_names = app.state.target_names

        if target_names is not None:
            predicted_label = str(target_names[predicted_class])
        else:
            predicted_label = f"class_{predicted_class}"

        return {
            "success": True,
            "prediction": predicted_class,
            "predicted_class": predicted_label,
            "message": f"Le vin appartient à la classe {predicted_label}"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la prédiction : {str(error)}"
        )