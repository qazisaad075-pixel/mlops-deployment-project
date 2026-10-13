
def runMLStage(String command) {
    echo "Executing Shared Library Stage Command: ${command}"
    bat command
}

pipeline {
    agent any

    stages {
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Install Dependencies") {
            steps {
                bat """
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage("Dev Pipeline") {
            when {
                branch "dev"
            }
            stages {
                stage("Data Ingest & Model Train") {
                    steps {
                        script {
                            runMLStage("python src/train.py")
                            runMLStage("python src/train_logistic.py")
                        }
                    }
                }
            }
        }

        stage("Pre-Prod Pipeline") {
            when {
                branch "main"
            }
            stages {
                stage("Load & Validate Challenger Model") {
                    steps {
                        script {
                            runMLStage("python src/pre_prod_test.py")
                        }
                    }
                }
            }
        }

        stage("Prod Pipeline") {
            when {
                buildingTag()
            }
            stages {
                stage("Promote Model to Champion") {
                    steps {
                        script {
                            echo "Running Prod Pipeline for Release Tag..."
                            runMLStage("python src/prod_deploy.py")
                        }
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline Failed! Sending Notification..."
        }
    }
}
