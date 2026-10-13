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

        // ==========================================
        // 1. DEV PIPELINE (Triggers on 'dev' branch)
        // ==========================================
        stage('Dev Pipeline') {
            when {
                branch 'dev'
            }
            stages {
                stage('Data Ingest & Model Train') {
                    steps {
                        bat 'python src/train.py'
                    }
                }
                stage('Model Test & Evaluation') {
                    steps {
                        bat '''
                            python -c "import mlflow; client = mlflow.tracking.MlflowClient(); exp = client.get_experiment_by_name('MLOps_Disease_Classification'); run = client.search_runs(exp.experiment_id)[0]; acc = run.data.metrics['accuracy']; print(f'Dev Accuracy: {acc}'); assert acc >= 0.90, 'Accuracy below threshold!'"
                        '''
                    }
                }
            }
        }

        // ==========================================
        // 2. PRE-PROD PIPELINE (Triggers on 'main' branch)
        // ==========================================
        stage('Pre-Prod Pipeline') {
            when {
                branch 'main'
            }
            steps {
                echo 'Running Pre-Prod Pipeline for Main Branch...'
                // Pre-prod loading and re-aliasing script next step mein add karenge
            }
        }

        // ==========================================
        // 3. PROD PIPELINE (Triggers on Release Tag)
        // ==========================================
        stage('Prod Pipeline') {
            when {
                buildingTag()
            }
            steps {
                echo 'Running Prod Pipeline for Release Tag...'
                // Prod loading and Champion aliasing script next step mein add karenge
            }
        }
    }

    post {
        failure {
            echo 'Pipeline Failed! Sending Email Notification...'
            // Failure notification logic
        }
    }
}