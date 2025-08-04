# 🛋 Domus Aurea — мебельный e-commerce на Django

Привет! 👋 Рад, что вы заинтересовались этим проектом.

**Domus Aurea** — это полнофункциональная e-commerce платформа для продажи мебели, разработанная на Django и Django REST Framework. Проект полностью контейнеризирован с помощью Docker и готов к развертыванию.

## 🛠 Технологический стек

### Backend
- Python 3.11
- Django
- Django REST Framework

### База данных
- PostgreSQL

### Frontend
- HTML
- Tailwind CSS
- Alpine.js (для легковесной интерактивности)

### Дополнительные компоненты
- Celery (фоновые задачи)
- Redis (брокер сообщений и кэширование)
- DRF-Spectacular (документация Swagger/Redoc)
- Simple JWT (аутентификация)

### Инфраструктура
- Docker + Docker Compose
- GitHub Actions (CI/CD)

### Тестирование
- Django TestCase
- factory-boy + Faker (генерация тестовых данных)

## 🚀 Быстрый старт

### Предварительные требования
- Установленные Docker и Docker Compose
- Git

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Elisei0p4/Domus-Aurea.git
```
2.Перейдите в директорию проекта:
```bash
cd Domus-Aurea
```
3. Настройте окружение:
```bash
cp .env.example .env
```
4. Запустите сервисы:
```bash
docker-compose up --build
```
5.Примените миграции:
```bash
docker-compose exec web python manage.py migrate
```
6. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```
7.Заполните базу тестовыми данными:
```bash
docker-compose exec web python manage.py seed_db
```

### Тестирование

Для запуска тестов выполните:

```bash
docker-compose exec web python manage.py test
```

> **Примечание**: Этот проект находится в активной разработке.  
> [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
> [![Django](https://img.shields.io/badge/Django-4.2.8-informational)](https://djangoproject.com)
