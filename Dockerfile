# Шаг 1: Используем официальный образ Python как базовый
# версия - легкая, хорошо подходит для production
FROM python:3.11-slim

# Шаг 2: Установка системных окружения
# PYTHONUNBUFFERED: гарантирует, что вывод Python сразу попадает в логги Docker
# PYTHONDONTWRITEBYTECODE: не создает .pyc файлы
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt


COPY . .

EXPOSE 8000


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "furniture.wsgi"]