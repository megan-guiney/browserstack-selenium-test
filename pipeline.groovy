pipeline {
    agent any

    environment {

        BROWSERSTACK_LOCAL = 'false'
        BROWSERSTACK_USERNAME = credentials('BROWSERSTACK_JENKINS_USER')
        BROWSERSTACK_ACCESS_KEY = credentials('BROWSERSTACK_JENKINS_KEY')
        DEMO_USER = credentials('DEMO_TEST_USER')
        DEMO_PASSWORD = credentials('DEMO_TEST_PASSWD')
    }
          

    stages {
        
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'e14e3bb2-2681-4b50-a0f8-c48ef6635aac',
                    url: 'https://github.com/megan-guiney/browserstack-selenium-test'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    if [ ! -d "venv" ]; then
                        python3.8 -m venv venv               # Create virtual environment
                    fi
                    . venv/bin/activate         # Activate virtual environment
                    python3.8 -m pip install --upgrade pip        # Ensure pip is up-to-date
                    python3.8 -m pip install -r requirements.txt  # Install required dependencies
                    '''
                  
                
            }
        }

        stage('Run Selenium Tests on BrowserStack') {
            steps {
                sh '. venv/bin/activate'
                sh 'browserstack-sdk pytest test_browserstack_demo.py'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '**/test-reports/*.xml', allowEmptyArchive: true
        }
        cleanup {
                sh '''
                    echo "Cleaning up BrowserStack Local process..."
                    pkill -f BrowserStackLocal || echo "No process found"
                '''
        }
    }
}
