import os
import pandas as pd
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# Same Absolute Central MLflow Tracking URI
db_path = os.path.abspath("C:/Users/AhmadLap/mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{db_path}")

def validate_pre_prod():
    print("--- Pre-Prod Pipeline Execution ---")
    model_name = "Disease_Classification_Model"
    client = MlflowClient()

    try:
        # Load model using 'Challenger' alias
        model_uri = f"models:/{model_name}@Challenger"
        model = mlflow.sklearn.load_model(model_uri)
        
        # Get version info
        model_version_info = client.get_model_version_by_alias(model_name, "Challenger")
        version_num = model_version_info.version
        
        # Set 'Challenger pre-test' alias before validation
        client.set_registered_model_alias(model_name, "Challenger pre-test", version_num)
        print(f"Model version {version_num} loaded and alias set to 'Challenger pre-test'")

        # Load test data and validate
        data_path = "data/disease_data.csv"
        df = pd.read_csv(data_path)
        X = df.drop(columns=["target"])
        y = df["target"]

        preds = model.predict(X)
        acc = accuracy_score(y, preds)
        print(f"Pre-Prod Model Validation Accuracy: {acc:.4f}")

        # Quality Gate (Threshold >= 0.90)
        if acc >= 0.90:
            client.set_registered_model_alias(model_name, "Challenger post-test", version_num)
            print(f"Validation Passed! Updated alias to 'Challenger post-test' for version {version_num}")
        else:
            raise ValueError(f"Accuracy {acc:.4f} is below the required 0.90 threshold.")

    except Exception as e:
        print(f"Error in Pre-Prod validation: {e}")
        raise e

if __name__ == "__main__":
    validate_pre_prod()