Проект мебельного магазина "Domus Aurea"
Привет! Рад, что ты заглянул в репозиторий этого проекта.
"Domus Aurea" — это полнофункциональный веб-проект, представляющий собой e-commerce платформу для продажи мебели. Проект разработан на Django и Django REST Framework, полностью контейнеризирован с помощью Docker и готов к развертыванию. (нет, писал не чат-жыпыты)

## Стек проекта:

1. Backend : Python 3.11, Django, Django REST Framework
2. База данных : PostgreSQL
3. Frontend :	HTML, Tailwind CSS, Alpine.js (для легковесной интерактивности)
4. Асинхронность : Celery (для фоновых задач), Redis (как брокер сообщений для Celery и для кэширования)
5. API : DRF-Spectacular (документация Swagger/Redoc), Simple JWT (аутентификация)
6. Контейнеризация : Docker, Docker Compose
7. Тестирование :	Django TestCase, factory-boy & Faker (для генерации тестовых данных)
8. CI/CD : GitHub Actions


## Пошаговый запуск моего проекта:

1. git clone https://github.com/Elisei0p4/Domus-Aurea.git

2. cd Domus-Aurea

3. cp .env.example .env

4. docker-compose up --build

5. docker-compose exec web python manage.py createsuperuser

6. docker-compose exec web python manage.py seed_db

## Страница доступна по адресу http://127.0.0.1:8000


## Тестирование (если нужно):

1. docker-compose exec web python manage.py test
