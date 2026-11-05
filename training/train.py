from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score,StratifiedKFold 
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

wine = load_wine(as_frame=True)
X = wine.data      # les 13 caractéristiques
y = wine.target    # la classe (0, 1 ou 2)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(X_train.shape, X_test.shape)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])

pipeline.fit(X_train, y_train)
print("Accuracy test :", pipeline.score(X_test, y_test))

# Comparaison de 5 algorihmes par validation croisée
models= {
    "Regression logistique":LogisticRegression(max_iter=1000),
    "Forêt aléatoire":RandomForestClassifier(random_state=42),
    "SVM":SVC(),
    "KNN":KNeighborsClassifier(),
    "Arbre de décision":DecisionTreeClassifier(random_state=42),
}

cv= StratifiedKFold(n_splits=5,shuffle=True,random_state=42)

import pandas as pd
resultats=[]
for name,model in models.items():
    pipe= Pipeline([("scaler",StandardScaler()),("model",model)])
    scores= cross_val_score(pipe,X,y,cv=cv,scoring="accuracy")
    resultats.append({
        "Algorithme":name,
        "Score moyen":round(scores.mean(),3),
        "Ecart (+/-)":round(scores.std(),3),
    })

tableau= pd.DataFrame(resultats).sort_values("Score moyen",ascending=False)
print(tableau.to_string(index=False))

import joblib
best_model= Pipeline([
    ("scaler",StandardScaler()),
    ("model",LogisticRegression(max_iter=1000)),
])
best_model.fit(X,y)
joblib.dump(best_model,"models/wine_model.joblib")
print("Modèle sauvegardé dans models/wine_model.joblib")
