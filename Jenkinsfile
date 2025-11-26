pipeline {
    agent {
        docker {
            image 'python:3.13.9-slim'
            args '--network jenkins-network -v /var/jenkins_home/workspace/API_Test:/app'
        }
    }

    tools {
        allure 'allure'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install -r /app/requirements.txt
                '''
            }
        }

        stage('Run Tests With Allure') {
            steps {
                sh '''
                    pytest /app/test_api.py -v --alluredir=/app/allure-results
                '''
            }
        }
    }
    
    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
