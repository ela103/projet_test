pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${env.WORKSPACE}"
    }

    stages {
        stage('Checkout Repository') {
            steps {
                git url: 'https://github.com/ela103/projet_test.git', branch: 'master'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install selenium'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Workspace path: ${env.WORKSPACE}"

                // Exécuter les trois fichiers EXACTEMENT comme ils sont dans GitHub
                bat 'python Add_To_Cart.py'
                bat 'python UI_Product.py'
                bat 'python Header_Footer.py'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé !'
        }
        success {
            echo 'Tous les tests ont été exécutés avec succès.'
        }
        failure {
            echo 'Certains tests ont échoué. Vérifie le log.'
        }
    }
}
