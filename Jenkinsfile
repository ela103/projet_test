pipeline {
    agent any

    environment {
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

        stage('Run Selected Python Tests') {
            steps {
                script {
                    def testFiles = ["Add_to_cart.py", "UI_Product.py", "Header_Footer.py"]

                    for (file in testFiles) {
                        bat """
                        echo -------------------------------
                        echo Running ${file}
                        python ${file}
                        if errorlevel 1 (
                            echo ${file} a échoué mais on continue
                        ) else (
                            echo ${file} exécuté avec succès
                        )
                        echo -------------------------------
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé !'
        }
        success {
            echo 'Tous les scripts ont été exécutés avec succès.'
        }
        failure {
            echo 'Certains scripts ont échoué. Vérifie le log pour voir lesquels.'
        }
    }
}
