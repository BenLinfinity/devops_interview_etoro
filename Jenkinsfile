pipeline {
    agent none
        environment {
            AKS_SERVER = 'https://devops-interview-cnxosza8.hcp.westeurope.azmk8s.io:443'
            AKS_SERVER_ID = '6dae42f8-4368-4678-94ff-3960e28e3630'
            HELM_RELEASE_NAME = 'simple-web'
        }
        parameters {
            choice(name: 'ACTION', choices: ['Deploy','Destroy'])
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
                            sh "set +x && kubectl config set-credentials msi-user --token=${env.KUBE_TOKEN} && set -x"
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
                            sh 'helm lint --strict ./helm/simple-web' // Checks helm syntax and missing values
                            sh 'helm template simple-web ./helm/simple-web | kubectl apply --dry-run=client --validate=strict -f -' // Checks rendered manifests for k8s syntax fails fast
                            withCredentials([string(credentialsId: 'image-pull-secret', variable: 'IMAGE_PULL_SECRET')]) {
                                sh "helm upgrade --install ${env.HELM_RELEASE_NAME} ./helm/simple-web --dry-run=server --debug --namespace benl --set secretValue=$IMAGE_PULL_SECRET"
                            }
                        }
                    }
                }

                stage('Safety Check') {
                    when { expression { params.ACTION == 'Destroy' } }
                    steps {
                        input message: 'WARNING! You are about to destroy all resources managed by this pipeline! \
                        Are you sure?', ok:'YES, DESTROY'
                    }
                }

                stage('Destroy') {
                    when { expression { params.ACTION == 'Destroy' } }
                    steps {
                        container('kubectl') {
                            sh "helm uninstall ${env.HELM_RELEASE_NAME} --namespace benl 2>&1 || true"
                        }
                    }
                }
                stage('Deploy') {
                    when { expression { params.ACTION == 'Deploy' } }
                    steps {
                        container('kubectl') {
                            timeout(time: 24, unit: 'HOURS') {
                                input message: 'Deploy to cluster?', ok: 'Deploy'
                            }
                            withCredentials([string(credentialsId: 'image-pull-secret', variable: 'IMAGE_PULL_SECRET')]) {
                                sh "helm upgrade --install ${env.HELM_RELEASE_NAME} ./helm/simple-web --namespace benl --wait --timeout 3m --rollback-on-failure --set secretValue=$IMAGE_PULL_SECRET"
                            }
                        }
                    }
                }
                // stage('Smoke Test') {
                //     when { expression { params.ACTION == 'Deploy' } }
                //     steps {
                //         container('kubectl') {
                //             sh "kubectl run curl --rm -i --restart=Never --image=curlimages/curl -- curl -s http://${env.HELM_RELEASE_NAME}.benl.svc.cluster.local:80/healthz"
                //         }
                //     }
                // }
            }
        }
    }
}