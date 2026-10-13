import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

db_path = os.path.abspath("C:/Users/AhmadLap/mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{db_path}")

mlflow.set_experiment("Disease_Classification_Logistic")

def train_logistic():
    data_path = "data/disease_data.csv"
    if not os.path.exists(data_path):
        os.makedirs("data", exist_ok=True)
        X_dummy, y_dummy = make_classification(n_samples=200, n_features=5, random_state=42)
        df_dummy = pd.DataFrame(X_dummy, columns=[f"feature_{i}" for i in range(5)])
        df_dummy["target"] = y_dummy
        df_dummy.to_csv(data_path, index=False)

    df = pd.read_csv(data_path)
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model_name = "Logistic_Regression_Model"

    with mlflow.start_run():
        clf = LogisticRegression()
        clf.fit(X_train, y_train)

        acc = accuracy_score(y_test, clf.predict(X_test))
        mlflow.log_metric("accuracy", acc)

        result = mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="model",
            registered_model_name=model_name
        )
        
        client = MlflowClient()
        client.set_registered_model_alias(model_name, "Challenger", result.registered_model_version)
        print(f"Logged Logistic Regression version {result.registered_model_version} as Challenger")

if __name__ == "__main__":
    train_logistic()
