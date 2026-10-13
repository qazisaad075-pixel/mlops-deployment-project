pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Training Script') {
            steps {
                bat '''
                    python src/train.py
                '''
            }
        }

        stage('Evaluate Model Threshold') {
            steps {
                bat '''
                    python -c "import mlflow; client = mlflow.tracking.MlflowClient(); exp = client.get_experiment_by_name('MLOps_Disease_Classification'); run = client.search_runs(exp.experiment_id)[0]; acc = run.data.metrics['accuracy']; print(f'Latest Model Accuracy: {acc}'); assert acc >= 0.90, 'Accuracy is below 90% threshold!'"
                '''
            }
        }
    }
}