pipeline {
    agent any

    stages {
        stage('Клонирование проекта') {
            steps {
                git branch: 'main', url: 'git@github.com:5jantuan/test-for-authomation-and-scripting.git'
            }
        }

        stage('Копирование на тестовый сервер') {
            steps {
                sh '''
                rsync -avz --delete ./ ansible@172.18.0.4:/var/www/html/
                '''
            }
        }

        stage('Перезапуск Apache через Ansible') {
            steps {
                sh 'ansible-playbook ansible/setup_test_server.yml -i ansible/hosts.ini --tags "apache"'
            }
        }
    }
}
