🛋️ Domus-Aurea – Django E-Commerce Platform
<div align="center"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"> <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"> </div>
Современный интернет-магазин мебели с полным циклом заказа, блогом и REST API.

🚀 Быстрый старт
Предварительные требования
Git

Docker Desktop (убедитесь, что он запущен)

Пошаговая инструкция
1. Клонируйте репозиторий
bash
git clone https://github.com/Elisei0p4/furniture.git && cd furniture
2. Настройте окружение
bash
cp .env.example .env  # Linux/MacOS  
cmd
copy .env.example .env  # Windows CMD  
3. Запустите проект
bash
docker-compose up -d --build
*(Первая сборка займет 5-15 минут)*

4. Инициализируйте данные
bash
docker-compose exec web python manage.py seed_db
5. Создайте администратора
bash
docker-compose exec web python manage.py createsuperuser
🌐 Доступ к проекту
Сайт: http://localhost:8000

Админка: http://localhost:8000/admin

API Docs:

Swagger UI

ReDoc

🔧 Полезные команды
Действие	Команда
Остановить контейнеры	docker-compose down
Полный сброс (с удалением данных)	docker-compose down -v
Просмотр логов	docker-compose logs -f web
Запуск тестов	docker-compose exec web python manage.py test
🛠️ Технологический стек
Backend
Django + DRF (REST API)

Celery + Redis (асинхронные задачи)

Gunicorn (production-сервер)

Frontend
TailwindCSS (стили)

Alpine.js (интерактивность)

Инфраструктура
Docker + Docker Compose

GitHub Actions (CI/CD)

PostgreSQL (база данных)

🌟 Ключевые особенности
🛒 E-Commerce
Каталог с фильтрацией и поиском

Корзина, избранное, сравнение товаров

Оформление заказов с резервированием

📱 Пользовательский опыт
Личный кабинет с историей заказов

Адаптивный дизайн (mobile-first)

Асинхронные действия (без перезагрузки)

🛠️ Для разработчиков
Полноценное REST API с документацией

Готовые Docker-образы

Автоматическое тестирование

📦 Структура проекта
text
furniture/  
├── api/           # REST API (DRF)  
├── cart/          # Логика корзины  
├── blog/          # Контент-система  
├── static/        # CSS/JS (Tailwind)  
└── docker/        # Конфиги Docker  
🤝 Контакты
Автор: [Ваше Имя]
Email: [your.email@example.com]
LinkedIn: [ссылка]

⭐ Не забудьте поставить звезду, если проект вам понравился!

<div align="center"> <sub>Разработано с ❤️ и Django</sub> </div>
🔄 Дополнительные настройки
Если нужно пересобрать статику:
bash
docker-compose exec web python manage.py collectstatic --no-input  
Миграции (при обновлении кода):
bash
docker-compose exec web python manage.py migrate  
Запуск shell:
bash
docker-compose exec web python manage.py shell  
Работодателю: Этот проект готов к немедленному запуску — просто следуйте инструкциям выше. Все зависимости изолированы в Docker, что гарантирует идентичную работу на любом компьютере. 🎯

