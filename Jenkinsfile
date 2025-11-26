pipeline {
    agent {
        docker {
            image 'python:3.13.9-slim'
            args '--network jenkins-network'
        }
    }

    tools {
        allure 'allure'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    cd /var/jenkins_home/workspace/API_Test
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests With Allure') {
            steps {
                sh '''
                    cd /var/jenkins_home/workspace/API_Test
                    pytest test_api.py -v --alluredir=allure-results
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
