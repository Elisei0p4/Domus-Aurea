# Устанавливает зависимости для сборки и сами Python-пакеты в виртуальное окружение.
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости, необходимые для СБОРКИ пакетов.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем только файлы с зависимостями и устанавливаем их.
# Этот слой будет кэшироваться, пока requirements.txt не изменится.
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Собираем финальный, более легкий образ для запуска приложения.
FROM python:3.11-slim as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# Устанавливаем системные зависимости, необходимые для ЗАПУСКА приложения.
# Делаем это в самом начале, чтобы слой максимально кэшировался.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Создаем пользователя без прав root для безопасности.
RUN addgroup --system django-user && adduser --system --ingroup django-user django-user

WORKDIR /app

# Копируем готовое виртуальное окружение из стадии сборки.
COPY --from=builder /opt/venv /opt/venv

# Копируем entrypoint отдельно, чтобы кэшировать этот шаг.
COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

# Копируем весь остальной код приложения.
# Этот слой будет пересобираться чаще всего, но он выполняется быстро.
COPY . .

# Создаем папки и назначаем права.
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R django-user:django-user /app

USER django-user

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "furniture.wsgi"]