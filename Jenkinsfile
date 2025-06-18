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
        stage('Check Environment & Dependencies') {
            steps {
                echo "🔍 Checking environment setup..."
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Pip version:"
                    pip3 --version

                    echo "Checking jinja2 installation..."
                    python3 -c "import jinja2; print('jinja2 version:', jinja2.__version__)" || echo "jinja2 not installed!"

                    echo "kubectl version:"
                    kubectl version --client --short || echo "kubectl not available!"
                '''
            }
        }

        stage('Install Missing Dependencies (optional)') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install jinja2
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Generate YAML Files') {
            steps {
                script {
                    writeFile file: 'params.env', text: """
                    service_name=${params.SERVICE_NAME}
                    image=${params.IMAGE}
                    port=${params.PORT}
                    replicas=${params.REPLICAS}
                    """
                    sh '''
                        source venv/bin/activate
                        python3 ${SCRIPT_DIR}/generate_yaml.py
                    '''
                }
            }
        }

        stage('Apply to KIND Cluster') {
            steps {
                sh '/usr/local/bin/kubectl apply -f rendered_yamls/deployment.yaml'
                sh 'kubectl apply -f rendered_yamls/service.yaml'
                sh 'kubectl apply -f rendered_yamls/virtualservice.yaml || true'
            }
        }
    }
}
