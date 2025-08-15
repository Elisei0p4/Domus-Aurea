#!/bin/sh
# Прерываем выполнение скрипта при любой ошибке
set -e

# Проверяем, доступны ли переменные окружения для подключения к БД
if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    echo "Waiting for database..."

    # Используем Python для проверки TCP-соединения, так как он точно есть в образе
    # Это надежнее, чем просто ждать фиксированное время (sleep)
    while ! python -c "import socket; import os; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((os.environ['DB_HOST'], int(os.environ['DB_PORT'])))" > /dev/null 2>&1; do
      echo "Database is unavailable - sleeping"
      sleep 1
    done

    echo "Database is up - executing command"
fi

# Выполняем команду, переданную в docker-compose (например, gunicorn или migrate)
exec "$@"