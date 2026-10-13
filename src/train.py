import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# 1. Dataset Load Karein
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# 2. MLflow Experiment Set Karein
mlflow.set_experiment("MLOps_Disease_Classification")

model_name = "Disease_Classification_Model"

with mlflow.start_run() as run:
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    acc = clf.score(X_test, y_test)
    mlflow.log_metric("accuracy", acc)
    
    # Model Log Karein
    model_info = mlflow.sklearn.log_model(
        clf, 
        name="model", 
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )
    print(f"Model trained successfully with Accuracy: {acc}")

    # 3. Model Registry Mein Save & 'Challenger' Alias Assign Karein
    client = MlflowClient()
    
    # Model Register Karein
    model_uri = f"runs:/{run.info.run_id}/model"
    reg_model = mlflow.register_model(model_uri, model_name)
    
    # Alias 'Challenger' Assign Karein
    client.set_registered_model_alias(
        name=model_name,
        alias="Challenger",
        version=reg_model.version
    )
    print(f"Model Version {reg_model.version} registered with alias 'Challenger'")