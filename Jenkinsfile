pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ishaangupta23/fraud-detection"
        DOCKER_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                // Jenkins pulls your code from GitHub
                checkout scm
            }
        }

        stage('Test') {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    steps {
        sh '''
            pip install -r requirements.txt
            pip install pytest httpx
            pytest tests/ -v
        '''
    }
}

        stage('Build Docker Image') {
            steps {
                // builds the image inside the Jenkins container
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // uses credentials stored in Jenkins — never hardcode passwords
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ishaangupta23/fraud-detection:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // applies your k8s manifests — same commands you ran manually
                sh '''
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/hpa.yaml
                    kubectl rollout status deployment/fraud-detection
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed — new version deployed to Kubernetes'
        }
        failure {
            echo 'Pipeline failed — check the logs above'
        }
    }
}