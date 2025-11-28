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

        stage('Run All Python Tests') {
            steps {
                echo 'Exécution de tous les scripts Python (.py) du dossier...'
                bat '''
                for %%f in (*.py) do (
                    echo -------------------------------
                    echo Running %%f
                    python %%f
                    if %ERRORLEVEL% neq 0 (
                        echo %%f a échoué mais on continue
                    ) else (
                        echo %%f exécuté avec succès
                    )
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
        success {
            echo 'Tous les scripts ont été exécutés. Vérifie le log pour PASS/FAIL par test.'
        }
        failure {
            echo 'Certains scripts ont échoué. Vérifie le log pour voir lesquels.'
        }
    }
}
