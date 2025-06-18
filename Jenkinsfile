pipeline {
    agent any

    parameters {
        string(name: 'SERVICE_NAME', defaultValue: 'my-app', description: 'Service Name')
        string(name: 'IMAGE', defaultValue: 'nginx:latest', description: 'Container Image')
        string(name: 'PORT', defaultValue: '80', description: 'Port')
        string(name: 'REPLICAS', defaultValue: '2', description: 'Replica Count')
    }

    environment {
        SCRIPT_DIR = 'scripts'
    }

    stages {
        stage('Generate YAML Files') {
            steps {
                script {
                    writeFile file: 'params.env', text: """
                    service_name=${params.SERVICE_NAME}
                    image=${params.IMAGE}
                    port=${params.PORT}
                    replicas=${params.REPLICAS}
                    """

                    sh "python3 ${env.SCRIPT_DIR}/generate_yaml.py"
                }
            }
        }

        stage('Apply to KIND Cluster') {
            steps {
                sh 'kubectl apply -f rendered_yamls/deployment.yaml'
                sh 'kubectl apply -f rendered_yamls/service.yaml'
                sh 'kubectl apply -f rendered_yamls/virtualservice.yaml || true'
            }
        }
    }
}
