pipeline {
    agent any

    stages {
        stage('Клонирование Ansible репозитория') {
            steps {
                git branch: 'main', url: 'git@github.com:5jantuan/test-for-authomation-and-scripting.git'
            }
        }

        stage('Выполнение Ansible плейбука') {
            steps {
                sh 'ansible-playbook ansible/setup_test_server.yml -i ansible/hosts.ini'
            }
        }
    }
}
