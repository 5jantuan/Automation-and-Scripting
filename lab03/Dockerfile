# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем cron и зависимости
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем скрипт и конфиги
COPY currency_exchange_rate.py .
COPY cronjob .
COPY entrypoint.sh .

# Устанавливаем Python-библиотеки, если есть requirements.txt
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Добавляем cronjob
RUN crontab /app/cronjob

# Запуск entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
