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
                        -t ghcr.io/taymie-biyi/jastl-devops:${BUILD_NUMBER} \
                        -t ghcr.io/taymie-biyi/jastl-devops:latest .
                '''
            }
        }

        stage('Login to GHCR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-pat',
                        usernameVariable: 'GITHUB_USER',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$GITHUB_TOKEN" | docker login ghcr.io \
                            -u "$GITHUB_USER" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push ghcr.io/taymie-biyi/jastl-devops:${BUILD_NUMBER}
                    docker push ghcr.io/taymie-biyi/jastl-devops:latest
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker ps -aq \
                        --filter "name=^jastl-devops-app$" \
                        | xargs -r docker rm -f

                    sleep 2

                    docker pull ghcr.io/taymie-biyi/jastl-devops:latest

                    docker run -d \
                        --name jastl-devops-app \
                        --restart unless-stopped \
                        -p 8085:5000 \
                        ghcr.io/taymie-biyi/jastl-devops:latest
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

        stage('Logout from GHCR') {
            steps {
                sh '''
                    docker logout ghcr.io || true
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

        always {
            sh 'docker logout ghcr.io || true'
        }
    }
}
