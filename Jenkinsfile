pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/taymie-biyi/jastl-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t jastl-devops .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f jastl-web || true
                    docker run -d \
                        --name jastl-web \
                        -p 8085:80 \
                        jastl-devops
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'curl -f http://localhost:8085'
            }
        }
    }

    post {
        success {
            echo 'JASTL DevOps deployment completed successfully.'
        }

        failure {
            echo 'JASTL DevOps deployment failed. Check the Jenkins console output.'
        }
    }
}
