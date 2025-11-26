pipeline {
    agent {
        label 'python-agent'
    }

    tools {
        allure 'allure'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests With Allure') {
            steps {
                sh '''
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
