pipeline {
    agent any

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

        stage('Run All Python Tests') {
            steps {
                echo 'Exécution de tous les scripts Python (.py) du dossier...'
                bat '''
                for %%f in (*.py) do (
                    echo -------------------------------
                    echo Running %%f
                    python %%f || echo %%f a échoué mais on continue
                    echo -------------------------------
                )
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé !'
        }
    }
}
