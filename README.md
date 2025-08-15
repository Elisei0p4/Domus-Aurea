🌟 Ключевые особенности проекта
✅ Каталог товаров: Продвинутая фильтрация, сортировка и поиск по товарам.
✅ Асинхронные действия: Добавление в корзину, избранное и сравнение без перезагрузки страницы.
✅ Личный кабинет: Просмотр истории заказов, управление личными данными.
✅ Система заказов: Оформление заказа с автоматическим списанием товаров со склада.
✅ REST API: Полноценный API на Django Rest Framework с документацией Swagger/Redoc.
✅ Контент-блог: Статьи, теги и система комментирования для вовлечения пользователей.
✅ Адаптивный дизайн: Современный интерфейс с использованием TailwindCSS и Alpine.js.
✅ Фоновые задачи: Использование Celery и Redis для отправки email-уведомлений.
✅ Полная Docker-изоляция: Весь проект и его зависимости запускаются в контейнерах.
✅ Автоматизация CI/CD: Настроенный workflow в GitHub Actions для линтинга и тестирования.
🛠️ Стек технологий
Категория	Технология
Backend	Django, Django REST Framework, Celery, Gunicorn
База данных	PostgreSQL
Кэш / Брокер	Redis
Frontend	HTML, TailwindCSS, Alpine.js
DevOps	Docker, Docker Compose, GitHub Actions
Тестирование	unittest (Django's default), factory-boy, Faker
🚀 Быстрый старт и развертывание
Проект полностью контейнеризирован с помощью Docker. Для запуска не требуется установка Python, PostgreSQL или Redis на вашу хост-систему.
Предварительные требования
Git: Скачать и установить
Docker Desktop: Скачать и установить (убедитесь, что он запущен)
Пошаговая инструкция по запуску
Клонируйте репозиторий:
Откройте терминал и выполните команду:
code
Bash
git clone https://github.com/Elisei0p4/furniture.git
Перейдите в папку проекта:
code
Bash
cd furniture
Создайте файл окружения .env:
Скопируйте файл-шаблон .env.example. Все необходимые значения для локального запуска уже установлены.
<details>
<summary>Команда для Windows (CMD / PowerShell)</summary>
code
Bash
copy .env.example .env
</details>
<details>
<summary>Команда для Linux / macOS</summary>
code
Bash
cp .env.example .env
</details>
Соберите образы и запустите контейнеры:
Эта команда скачает все зависимости, создаст образы и запустит все сервисы в фоновом режиме. Первый запуск может занять 5-15 минут.
code
Bash
docker-compose up -d --build
Наполните базу данных тестовым контентом:
Проект содержит команду для автоматического создания категорий, товаров, статей и т.д.
code
Bash
docker-compose exec web python manage.py seed_db
Создайте суперпользователя (администратора):
Вам будет предложено ввести логин, email и пароль для доступа к админ-панели.
code
Bash
docker-compose exec web python manage.py createsuperuser
🎉 Готово! Проект запущен и готов к работе.
Сайт: http://localhost:8000
Админ-панель: http://localhost:8000/admin/
⚙️ Полезные команды Docker
Все команды выполняются из корневой папки проекта (/furniture).
Остановить все контейнеры
code
Bash
docker-compose down
Остановить контейнеры и удалить все данные (тома)
Используйте эту команду для полного сброса проекта (база данных будет очищена).
code
Bash
docker-compose down -v
Просмотр логов
Очень полезно для отладки. Чтобы посмотреть логи веб-сервера в реальном времени:
code
Bash
docker-compose logs -f web
Нажмите Ctrl + C, чтобы выйти.
Выполнение management-команд Django
Любая команда manage.py выполняется через docker-compose exec:
code
Bash
docker-compose exec web python manage.py <ваша_команда>
🧪 Тестирование
Для запуска всего набора тестов выполните команду:
code
Bash
docker-compose exec web python manage.py test
📖 Документация API
Проект включает автогенерируемую документацию для REST API. После запуска проекта она доступна по следующим адресам:
Swagger UI: http://localhost:8000/api/schema/swagger-ui/
Redoc: http://localhost:8000/api/schema/redoc/
