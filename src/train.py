import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# Absolute Central MLflow Tracking URI to avoid multi-workspace path issues
db_path = os.path.abspath("C:/Users/AhmadLap/mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{db_path}")

mlflow.set_experiment("Disease_Classification_Experiment")

def train():
    # Load dataset
    data_path = "data/disease_data.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    df = pd.read_csv(data_path)
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_name = "Disease_Classification_Model"

    with mlflow.start_run() as run:
        params = {"n_estimators": 100, "max_depth": 5, "random_state": 42}
        clf = RandomForestClassifier(**params)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        prec = precision_score(y_test, predictions, average="weighted")
        rec = recall_score(y_test, predictions, average="weighted")
        f1 = f1_score(y_test, predictions, average="weighted")

        mlflow.log_params(params)
        mlflow.log_metrics({"accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1})

        # Log and Register Model
        result = mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="model",
            registered_model_name=model_name
        )
        
        client = MlflowClient()
        model_version = result.registered_model_version
        
        # Set 'Challenger' alias for the newly trained model version
        client.set_registered_model_alias(
            name=model_name,
            alias="Challenger",
            version=model_version
        )
        print(f"Successfully registered model version {model_version} with alias 'Challenger'")

if __name__ == "__main__":
    train()