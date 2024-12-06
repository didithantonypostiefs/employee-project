pipeline {
    agent { label 'employeemanagement-192.168.209.9' }
    stages {
        stage('Deploy') { 
            steps {
                sh './jenkins/scripts/deploy.sh'  
            }
        }
    }
}
