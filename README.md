<div align="center">

  <!-- Можете заменить этот URL на свой собственный баннер или логотип -->
  <img src="https://raw.githubusercontent.com/Elisei0p4/Domus-Aurea/main/assets/logo.png" alt="Domus Aurea Logo" width="600"/>

  <h1>🛋️ Domus Aurea</h1>

  <p><strong>Премиум мебельный e-commerce на Django, созданный с вниманием к деталям.</strong></p>
  
  <p>
    <a href="https://www.djangoproject.com/">
      <img src="https://img.shields.io/badge/Django-5.0-092E20?logo=django" alt="Django">
    </a>
    <a href="https://www.postgresql.org/">
      <img src="https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql" alt="PostgreSQL">
    </a>
    <a href="https://www.docker.com/">
      <img src="https://img.shields.io/badge/Docker-25.0-2496ED?logo=docker" alt="Docker">
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python" alt="Python">
    </a>
    <a href="https://github.com/Elisei0p4/Domus-Aurea/actions/workflows/ci.yml">
      <img src="https://github.com/Elisei0p4/Domus-Aurea/actions/workflows/ci.yml/badge.svg" alt="CI/CD Status">
    </a>
  </p>

</div>

---

## 📖 Оглавление

- [🏛️ О проекте](#️-о-проекте)
- [✨ Ключевые особенности](#-ключевые-особенности)
- [🛠️ Технологический стек](#️-технологический-стек)
- [🚀 Быстрый старт](#-быстрый-старт)
  - [📋 Предварительные требования](#-предварительные-требования)
  - [🔧 Установка и запуск](#-установка-и-запуск)
- [📚 API Документация](#-api-документация)
- [🧪 Тестирование](#-тестирование)
- [🗂️ Структура проекта](#️-структура-проекта)
- [🤝 Участие в разработке](#-участие-в-разработке)
- [📄 Лицензия](#-лицензия)

---

## 🏛️ О проекте

**Domus Aurea** — это полнофункциональная, готовая к развертыванию e-commerce платформа для продажи мебели премиум-класса. Проект построен на надежном стеке Django и Django REST Framework и полностью контейнеризирован с помощью Docker для легкого запуска и масштабирования.

> Привет! 👋 Рад, что вы заинтересовались этим проектом. Моя цель — создать не просто работающий магазин, а элегантное и производительное решение, которое будет приятно использовать как покупателям, так и администраторам.

<br>
<div align="center">
  <!-- Здесь можно разместить скриншот главного экрана вашего приложения -->
  <img src="https://raw.githubusercontent.com/Elisei0p4/Domus-Aurea/main/assets/screenshot.png" alt="Скриншот приложения" width="800"/>
</div>
<br>

---

## ✨ Ключевые особенности

- ✅ **Каталог товаров:** Удобная навигация по категориям, фильтрация и поиск.
- ✅ **Аутентификация пользователей:** Регистрация, вход и управление профилем на основе JWT.
- ✅ **Корзина и заказы:** Полноценный функционал для добавления товаров в корзину и оформления заказов.
- ✅ **Панель администратора:** Расширенная админ-панель Django для управления товарами, заказами и пользователями.
- ✅ **REST API:** Хорошо документированный API для возможной интеграции с фронтенд-фреймворками или мобильными приложениями.
- ✅ **Фоновые задачи:** Использование Celery для обработки асинхронных операций (например, отправки email).
- ✅ **CI/CD:** Автоматизированная проверка кода и запуск тестов с помощью GitHub Actions.

---

## 🛠️ Технологический стек

| Категория                | Технология                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| **Backend ⚙️**           | `Python 3.11`, `Django`, `Django REST Framework`                                                       |
| **Frontend 🎨**          | `HTML`, `Tailwind CSS`, `Alpine.js` (для легковесной интерактивности)                                  |
| **База данных 📦**       | `PostgreSQL`                                                                                           |
| **Кэш и брокер задач ⚡** | `Redis` (для Celery и кэширования)                                                                     |
| **Асинхронные задачи ⏳** | `Celery`                                                                                               |
| **API и Документация 📖** | `DRF-Spectacular` (Swagger/Redoc), `Simple JWT` (аутентификация)                                       |
| **Инфраструктура 🏗️**    | `Docker`, `Docker Compose`, `GitHub Actions` (CI/CD)                                                   |
| **Тестирование 🧪**      | `Django TestCase`, `factory-boy`, `Faker` (генерация тестовых данных)                                  |

---

## 🚀 Быстрый старт

Следуйте этим шагам, чтобы запустить проект локально.

### 📋 Предварительные требования

Убедитесь, что на вашей машине установлены:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

### 🔧 Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Elisei0p4/Domus-Aurea.git
    ```

2.  **Перейдите в директорию проекта:**
    ```bash
    cd Domus-Aurea
    ```

3.  **Настройте переменные окружения:**
    Скопируйте файл `.env.example` в `.env`. В нем уже есть все необходимые значения для локального запуска.
    ```bash
    cp .env.example .env
    ```

4.  **Соберите и запустите контейнеры:**
    Эта команда скачает образы, соберет ваши сервисы и запустит их в фоновом режиме.
    ```bash
    docker-compose up --build -d
    ```

5.  **Примените миграции базы данных:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

6.  **Создайте суперпользователя:**
    Чтобы получить доступ к админ-панели Django, создайте аккаунт администратора.
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

7.  **Заполните базу тестовыми данными (опционально):**
    Эта команда наполнит базу данных категориями и товарами для демонстрации.
    ```bash
    docker-compose exec web python manage.py seed_db
    ```

🎉 **Готово!** Проект доступен по адресам:
-   **Сайт:** [http://localhost:8000](http://localhost:8000)
-   **Админ-панель:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📚 API Документация

Проект использует `drf-spectacular` для автоматической генерации документации API. Она доступна после запуска проекта по следующим URL:

-   **Swagger UI:** [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
-   **ReDoc:** [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

## 🧪 Тестирование

Для запуска всего набора тестов выполните команду:
```bash
docker-compose exec web python manage.py test
