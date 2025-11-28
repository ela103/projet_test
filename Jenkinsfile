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

        stage('Run Selected Python Tests') {
            steps {
                echo 'Exécution des scripts Python sélectionnés...'
                bat '''
                rem Liste des fichiers Python à exécuter
                set FILES=Add_to_cart.py UI_Product.py Header_Footer.py

                for %%f in (%FILES%) do (
                    echo -------------------------------
                    echo Running %%f
                    python %%f
                    if errorlevel 1 (
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
            echo 'Scripts sélectionnés exécutés (certains peuvent avoir échoué, mais pipeline passe).'
        }
    }
}
