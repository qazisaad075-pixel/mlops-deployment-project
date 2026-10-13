import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

model_name = "Disease_Classification_Model"
client = MlflowClient()

print("--- Pre-Prod Pipeline Execution ---")

# 1. 'Challenger' Alias se Model Version Load Karein
try:
    model_version_info = client.get_model_version_by_alias(model_name, "Challenger")
    version = model_version_info.version
    print(f"Loaded model with alias 'Challenger' (Version: {version})")
except Exception as e:
    print(f"Error loading model with 'Challenger' alias: {e}")
    exit(1)

# 2. Assign Alias 'Challenger pre-test'
client.set_registered_model_alias(model_name, "Challenger pre-test", version)
print(f"Assigned alias 'Challenger pre-test' to Version {version}")

# 3. Pre-Prod Model Verification / Testing
print("Running Pre-Prod Model Validation...")
# Simulating model evaluation checks
run = client.get_run(model_version_info.run_id)
accuracy = run.data.metrics.get("accuracy", 0.0)

if accuracy >= 0.90:
    print(f"Pre-Prod Validation Passed with Accuracy: {accuracy}")
    # 4. Success Par Alias 'Challenger post-test' Update Karein
    client.set_registered_model_alias(model_name, "Challenger post-test", version)
    print(f"Successfully updated alias to 'Challenger post-test' for Version {version}")
else:
    raise Exception(f"Pre-Prod Validation Failed! Accuracy {accuracy} is below 0.90 threshold.")