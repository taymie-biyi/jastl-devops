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

        stage('Push Image to GHCR') {
            steps {
                sh '''
                    docker push ghcr.io/taymie-biyi/jastl-devops:${BUILD_NUMBER}
                    docker push ghcr.io/taymie-biyi/jastl-devops:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sshagent(credentials: ['k3s-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no jastlvm@192.168.59.68 \
                        "sudo -n /usr/local/bin/kubectl rollout restart deployment/jastl-devops && \
                        sudo -n /usr/local/bin/kubectl rollout status deployment/jastl-devops --timeout=120s"
                    '''
                }
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                sshagent(credentials: ['k3s-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no \
                            jastlvm@192.168.59.68 \
                            "sudo kubectl get deployment jastl-devops && \
                             sudo kubectl get pods -o wide -l app=jastl-devops && \
                             curl -f http://192.168.59.68:30085"
                    '''
                }
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
            echo 'JASTL DevOps Kubernetes deployment completed successfully.'
        }

        failure {
            echo 'JASTL DevOps deployment failed. Check the Jenkins console output.'
        }

        always {
            sh 'docker logout ghcr.io || true'
        }
    }
}
