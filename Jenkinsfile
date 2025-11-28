pipeline {
    agent any

    environment {
        // Tu peux ajouter ici des variables d'environnement si nécessaire
        WORKSPACE_DIR = "${env.WORKSPACE}"
    }

    stages {
        stage('Checkout Repository') {
            steps {
                // Cloner ton repo GitHub
                git url: 'https://github.com/ela103/projet_test.git', branch: 'master'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installer Selenium si nécessaire
                bat 'python -m pip install --upgrade pip'
                bat 'pip install selenium'
            }
        }

        stage('Run Tests') {
            steps {
                // Exécuter ton script Python
                bat 'python Add_To_Cart.py'
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
