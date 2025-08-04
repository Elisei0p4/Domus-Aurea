<div id="top"></div>
<div align="center">

  <!-- Замените URL на свой собственный баннер/логотип. Рекомендуемый размер: 1280x640px -->
  <img src="https://raw.githubusercontent.com/Elisei0p4/Domus-Aurea/main/assets/logo.png" alt="Domus Aurea Banner">

  <h1 style="font-size: 3em; font-weight: bold; border-bottom: none;">
    🛋️ Domus Aurea
  </h1>

  <p><strong>Премиум мебельный e-commerce на Django, созданный с вниманием к деталям.</strong></p>
  
  <p>
    <!-- Статусы и версии -->
    <a href="https://github.com/Elisei0p4/Domus-Aurea/actions/workflows/ci.yml">
      <img src="https://github.com/Elisei0p4/Domus-Aurea/actions/workflows/ci.yml/badge.svg" alt="CI Status">
    </a>
    <img src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django" alt="Django">
    <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Docker-25.0-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  </p>
  
  <h4>
    <a href="#-о-проекте">О проекте</a> |
    <a href="#-ключевые-особенности">Особенности</a> |
    <a href="#-технологический-стек">Технологии</a> |
    <a href="#-быстрый-старт">Быстрый старт</a> |
    <a href="#api-документация">API</a>
  </h4>

</div>

---

## 🏛️ О проекте

**Domus Aurea** — это полнофункциональная, готовая к развертыванию e-commerce платформа для продажи мебели премиум-класса. Проект построен на надежном стеке Django и Django REST Framework и полностью контейнеризирован с помощью Docker для легкого запуска и масштабирования.

> Привет! 👋 Рад, что вы заинтересовались этим проектом. Моя цель — создать не просто работающий магазин, а элегантное и производительное решение, которое будет приятно использовать как покупателям, так и администраторам.

<br>
<div align="center">
  <!-- Здесь можно разместить скриншот главного экрана вашего приложения -->
  <img src="https://raw.githubusercontent.com/Elisei0p4/Domus-Aurea/main/assets/screenshot.png" alt="Скриншот приложения" width="800" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/>
</div>
<br>

---

## ✨ Ключевые особенности

-   ✅ **Современный каталог товаров:** Удобная навигация, фильтрация и поиск.
-   🔐 **Безопасная аутентификация:** Регистрация, вход и управление профилем на основе JWT.
-   🛒 **Полноценная корзина:** Полный цикл от добавления товара до оформления заказа.
-   ⚙️ **Мощная админ-панель:** Расширенная админка Django для управления всем контентом.
-   🔌 **Гибкий REST API:** Хорошо документированный API для интеграции с любым фронтендом.
-   🚀 **Асинхронные задачи:** Celery для фоновой обработки, например, отправки email-уведомлений.
-   🔄 **CI/CD Автоматизация:** Встроенный воркфлоу GitHub Actions для автоматической проверки кода.

---

## 🛠️ Технологический стек

Это основные технологии, которые приводят проект в движение.

| Категория | Технологии |
| :--- | :--- |
| **Backend** | <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="20" height="20"/> `Python 3.11` <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" alt="Django" width="20" height="20"/> `Django` <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/djangorest/djangorest-original.svg" alt="DRF" width="20" height="20"/> `Django REST Framework` |
| **Frontend** | <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" alt="HTML5" width="20" height="20"/> `HTML` <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/tailwindcss/tailwindcss-plain.svg" alt="Tailwind CSS" width="20" height="20"/> `Tailwind CSS` <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/alpinejs/alpinejs-original.svg" alt="Alpine.js" width="20" height="20"/> `Alpine.js` |
| **База данных** | <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" alt="PostgreSQL" width="20" height="20"/> `PostgreSQL` |
| **Задачи и кэш** | <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original.svg" alt="Redis" width="20" height="20"/> `Redis` <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/celery/celery-original.svg" alt="Celery" width="20" height="20"/> `Celery` |
| **Инфраструктура** | <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" alt="Docker" width="20" height="20"/> `Docker & Docker Compose` <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" alt="GitHub" width="20" height="20"/> `GitHub Actions` |
| **Тестирование** | `Django TestCase`, `factory-boy`, `Faker` |

---

## 🚀 Быстрый старт

### 📋 Предварительные требования

Прежде чем начать, убедитесь, что у вас установлены:
-   [**Git**](https://git-scm.com/downloads)
-   [**Docker**](https://www.docker.com/get-started)
-   [**Docker Compose**](https://docs.docker.com/compose/install/) (обычно идет вместе с Docker Desktop)

### 🔧 Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Elisei0p4/Domus-Aurea.git
    ```

2.  **Перейдите в директорию проекта:**
    ```bash
    cd Domus-Aurea
    ```

3.  **Настройте окружение:**
    ```bash
    cp .env.example .env
    ```

4.  **Соберите и запустите контейнеры в фоновом режиме:**
    ```bash
    docker-compose up --build -d
    ```

5.  **Выполните миграции базы данных:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

6.  **Создайте суперпользователя для доступа к админ-панели:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

7.  **(Опционально) Заполните базу тестовыми данными:**
    ```bash
    docker-compose exec web python manage.py seed_db
    ```

🎉 **Готово!** Проект запущен и доступен по адресам:
-   **Сайт:** [http://localhost:8000](http://localhost:8000)
-   **Админ-панель:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

<div align="center">

<h2 id="api-документация">📚 API Документация</h2>

<p>После успешного запуска проекта на вашем компьютере, документация будет доступна по локальным адресам:</p>

  <a href="http://localhost:8000/api/schema/swagger-ui/">
    <img src="https://img.shields.io/badge/Swagger%20UI-Документация-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger UI">
  </a>
    
  <a href="http://localhost:8000/api/schema/redoc/">
    <img src="https://img.shields.io/badge/ReDoc-Документация-red?style=for-the-badge&logo=redoc&logoColor=white" alt="ReDoc">
  </a>

</div>

---

<div align="center">

<h2 id="тестирование">🧪 Тестирование</h2>

<p>Для гарантии качества кода в проекте настроены тесты. Для их запуска выполните:</p>

```bash
docker-compose exec web python manage.py test
