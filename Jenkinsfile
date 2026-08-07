pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/taymie-biyi/jastl-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                    -t jastl-devops:${BUILD_NUMBER} \
                    -t jastl-devops:latest .
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker ps -aq --filter "name=^jastl-devops-app$" | xargs -r docker rm -f

                    sleep 2

                        docker run -d \
                        --name jastl-devops-app \
                        --restart unless-stopped \
                        -p 8085:5000 \
                        jastl-devops:latest
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 5

                    docker ps --filter name=jastl-devops-app

                    docker exec jastl-devops-app \
                    python -c "import urllib.request; r=urllib.request.urlopen('http://localhost:5000'); print('HTTP Status:', r.status)"
                '''
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
