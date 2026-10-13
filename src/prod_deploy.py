import os
import mlflow
from mlflow.tracking import MlflowClient

# Absolute Central MLflow Tracking URI
db_path = os.path.abspath("C:/Users/AhmadLap/mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{db_path}")

def promote_to_champion():
    print("--- Production Pipeline Execution ---")
    model_name = "Disease_Classification_Model"
    client = MlflowClient()

    try:
        # Get model version that passed Pre-Prod validation
        model_version_info = client.get_model_version_by_alias(model_name, "Challenger-post-test")
        version_num = model_version_info.version
        
        # Promote model to 'Champion' (Production)
        client.set_registered_model_alias(model_name, "Champion", version_num)
        print(f"Successfully promoted model version {version_num} to 'Champion' (Production)!")

    except Exception as e:
        print(f"Error in Production promotion: {e}")
        raise e

if __name__ == "__main__":
    promote_to_champion()