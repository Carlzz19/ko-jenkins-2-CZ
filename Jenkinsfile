pipeline {
    agent any

    tools {
        allure 'allure-manual'
    }

    stages {
        stage('Run Tests in Docker') {
            steps {
                script {
                    docker.image('python:3.13.9-slim').inside("--network jenkins-network") {
                        stage('Install Dependencies') {
                            sh '''
                                cd /var/jenkins_home/workspace/API_Test
                                ls -la
                                pip install -r requirements.txt
                            '''
                        }
                        
                        stage('Run Tests') {
                            sh '''
                                cd /var/jenkins_home/workspace/API_Test
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
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'target/allure-results']],
                // Tambahkan konfigurasi title di sini
                reportName: 'Laporan Test Custom Saya',
                title: 'Allure Report - Project Saya'
            ])
        }
    }
}
