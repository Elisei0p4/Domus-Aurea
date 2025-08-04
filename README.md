# ✨ DOMUS AUREA

  ![Header Banner](https://via.placeholder.com/1200x400/2d2d2d/ffffff?text=DOMUS+AUREA+PREMIUM+FURNITURE)
  
  [![Django](https://img.shields.io/badge/Django-5.2.4-092E20?logo=django)](https://www.djangoproject.com/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.5-336791?logo=postgresql)](https://www.postgresql.org/)
  [![Docker](https://img.shields.io/badge/Docker-28.3-2496ED?logo=docker)](https://www.docker.com/)




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
2. Перейдите в директорию проекта:
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
5. Примените миграции:
```bash
docker-compose exec web python manage.py migrate
```
6. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```
8. Заполните базу тестовыми данными:
```bash
docker-compose exec web python manage.py seed_db
```

### Тестирование

Для запуска тестов выполните:

```bash
docker-compose exec web python manage.py test
```
