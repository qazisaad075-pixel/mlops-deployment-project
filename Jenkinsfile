pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Dev Pipeline') {
            when {
                branch 'dev'
            }
            steps {
                echo 'Running Dev Pipeline...'
            }
        }
        stage('Pre-Prod Pipeline') {
            when {
                branch 'main'
            }
            steps {
                echo 'Running Pre-Prod Pipeline...'
            }
        }
        stage('Prod Pipeline') {
            when {
                tag pattern: "v*", comparator: "GLOB"
            }
            steps {
                echo 'Running Prod Pipeline...'
            }
        }
    }
}
