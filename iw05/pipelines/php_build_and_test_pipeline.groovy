pipeline {
    agent any

    stages {
        stage('Клонирование репозитория') {
            steps {
                git branch: 'main', url: 'git@github.com:5jantuan/test-for-authomation-and-scripting.git'
            }
        }

        stage('Установка зависимостей') {
            steps {
                sh 'composer install'
            }
        }

        stage('Запуск юнит-тестов') {
            steps {
                sh 'vendor/bin/phpunit --colors=always'
            }
        }

        stage('Отчет о тестах') {
            steps {
                junit 'tests/results/*.xml'
            }
        }
    }
}
