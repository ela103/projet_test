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
                echo 'Exécution de tous les scripts Python dans le projet...'
                // Exécuter tous les fichiers .py du répertoire
                bat '''
                for %%f in (*.py) do (
                    echo Running %%f
                    python %%f
                )
                '''
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
