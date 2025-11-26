pipeline {
    agent any

    tools {
        allure 'allure-manual'
    }

    stages {
        stage('Checkout and Run Tests in Docker') {
            steps {
                script {
                    docker.image('python:3.13.9-slim').inside("--network jenkins-network -v ${WORKSPACE}:/workspace") {
                        stage('Install Dependencies') {
                            sh '''
                                cd /workspace
                                pip install -r requirements.txt
                            '''
                        }
                        
                        stage('Run Tests') {
                            sh '''
                                cd /workspace
                                pytest test_api.py -v --alluredir=allure-results
                            '''
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Allure dijalankan di Jenkins host, bukan dalam Docker container
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
