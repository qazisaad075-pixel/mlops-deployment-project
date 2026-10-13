import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# Load Dataset
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

mlflow.set_experiment("MLOps_Disease_Classification")

with mlflow.start_run():
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    acc = clf.score(X_test, y_test)
    mlflow.log_metric("accuracy", acc)
    
    # Updated line: skops_trusted_types add kiya hai taaki untrusted type error na aaye
    mlflow.sklearn.log_model(clf, name="model", skops_trusted_types=["sklearn.tree._tree.Tree"])
    
    print(f"Model trained successfully with Accuracy: {acc}")