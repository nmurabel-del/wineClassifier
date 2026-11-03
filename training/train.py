from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

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