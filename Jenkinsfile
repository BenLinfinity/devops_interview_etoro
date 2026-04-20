pipeline {
    // agent any
    agent {
        kubernetes {
            cloud 'simple-app-agent'
            namespace 'benl'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: 'jenkins/inbound-agent:3355.v388858a_47b_33-19-jdk21'
  - name: helm
    image: alpine/helm:3.20.2
    command:
    - cat
    tty: true
"""
        }
    }


    stages {
        stage('SCM Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Lint') {
            steps {
                container('helm') {
                    sh 'helm lint --strict ./helm/simple-web'
                }
            }
        }
        stage('Deploy') {
            steps {
                container('helm') {
                    withCredentials([string(credentialsId: 'image-pull-secret', variable: 'IMAGE_PULL_SECRET')]) {
                    sh "helm upgrade --install simple-web ./helm/simple-web --namespace benl --set secretValue=$IMAGE_PULL_SECRET"
                    }
                }
            }
        }
    }
}