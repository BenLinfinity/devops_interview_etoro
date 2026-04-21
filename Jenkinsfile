pipeline {
    agent none
        environment {
            AKS_SERVER = 'https://devops-interview-cnxosza8.hcp.westeurope.azmk8s.io:443'
            AKS_SERVER_ID = '6dae42f8-4368-4678-94ff-3960e28e3630'
        }


    stages {
        stage('Get Token') {
            agent { label 'built-in' }
            steps {
                script {
                    env.KUBE_TOKEN = sh(
                        script: "az account get-access-token --resource ${env.AKS_SERVER_ID} --query accessToken -o tsv",
                        returnStdout: true
                        ).trim()
                }
            }
        }

        stage ('Pipeline') {
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
  - name: kubectl
    image: 'alpine/k8s:1.35.0'
    command:
    - cat
    tty: true
"""
        }
    }
        // The stages are nested to allow them to be run inside the pod
            stages {
                stage('Configure Permissions') {
                    steps {
                        container('kubectl') {
                            sh "kubectl config set-cluster aks --server=${env.AKS_SERVER} --insecure-skip-tls-verify=true"
                            sh "kubectl config set-credentials msi-user --token=${env.KUBE_TOKEN}"
                            sh "kubectl config set-context aks --cluster=aks --user=msi-user"
                            sh "kubectl config use-context aks"
                        }
                    }
                }
                stage('SCM Checkout') {
                    steps {
                        checkout scm
                    }
                }
                stage('Lint') {
                    steps {
                        container('kubectl') {
                            sh 'helm lint --strict ./helm/simple-web'
                        }
                    }
                }
                stage('Deploy') {
                    steps {
                        container('kubectl') {
                            timeout(time: 24, unit: 'HOURS') {
                                input message: 'Deploy to cluster?', ok: 'Deploy'
                            }
                            withCredentials([string(credentialsId: 'image-pull-secret', variable: 'IMAGE_PULL_SECRET')]) {
                            sh "helm upgrade --install simple-web ./helm/simple-web --namespace benl --set secretValue=$IMAGE_PULL_SECRET"
                            }
                        }
                    }
                }
            }
        }
    }
}