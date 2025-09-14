#!/bin/bash

# Проверка, передан ли хотя бы один аргумент
if [ -z "$1" ]; then
    echo "Ошибка: не указан каталог для очистки."
    echo "Использование: $0 <каталог> [расширения...]"
    exit 1
fi

TARGET_DIR="$1"
shift

if [ ! -d "$TARGET_DIR" ]; then
    echo "Ошибка: каталог '$TARGET_DIR' не существует."
    exit 1
fi

if [ $# -eq 0 ]; then
    EXTENSIONS=("*.tmp")
else
    EXTENSIONS=("$@")   # все оставшиеся аргументы — это расширения
fi


deleted=0


for ext in "${EXTENSIONS[@]}"; do
    count=$(find "$TARGET_DIR" -type f -name "$ext" -print -delete | wc -l)
    deleted=$((deleted + count))
done

echo "Удалено файлов: $deleted"
