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
    }
}