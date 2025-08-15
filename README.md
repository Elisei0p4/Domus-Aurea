# 🛋️ Domus Aurea – Django Furniture E-Commerce
<div align="center">
  <a href="https://www.djangoproject.com/" target="_blank">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  </a>
  <a href="https://www.postgresql.org/" target="_blank">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://tailwindcss.com/" target="_blank">
    <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS">
  </a>
  <a href="https://www.docker.com/" target="_blank">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
</div>

Современный интернет-магазин мебели с полным циклом заказа, блогом и REST API.

## 🌟 Ключевые особенности

### 🛒 E-Commerce
- Каталог с фильтрацией и поиском
- Корзина, избранное, сравнение товаров
- Оформление заказов с резервированием

### 📱 Пользовательский опыт
- Личный кабинет с историей заказов
- Адаптивный дизайн (mobile-first)
- Асинхронные действия (без перезагрузки)

### 🛠️ Для разработчиков
- Полноценное REST API с документацией
- Готовые Docker-образы
- Автоматическое тестирование

## 🛠️ Технологический стек


## 📸 Скриншоты
<div align="center">
  <img src="https://via.placeholder.com/800x400?text=Главная+страница" alt="Главная страница" width="400">
  <img src="https://via.placeholder.com/800x400?text=Каталог+товаров" alt="Каталог товаров" width="400">
</div>


**Backend**
- Django + DRF (REST API)
- Celery + Redis (асинхронные задачи)
- Gunicorn (production-сервер)

**Frontend**
- TailwindCSS (стили)
- Alpine.js (интерактивность)

**Инфраструктура**
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- PostgreSQL (база данных)

## 🚀 Быстрый старт

### Предварительные требования
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (убедитесь, что он запущен)

### Пошаговая инструкция

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/Elisei0p4/Domus-Aurea.git
   ```

2. **Настройте окружение**
   Для Linux
   ```bash
   cp .env.example .env
   ```
   Для Windows
   ```
   copy .env.example .env
   ```

4. **Запустите проект**
   ```bash
   docker-compose up -d --build
   ```

5. **Инициализируйте данные**
   ```bash
   docker-compose exec web python manage.py seed_db
   ```

6. **Создайте администратора**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### 🌐 Доступ к проекту
- 🌍 Сайт: [http://localhost:8000](http://localhost:8000)
- 🔐 Админка: [http://localhost:8000/admin](http://localhost:8000/admin)
- 📚 API Docs:
  - Swagger UI
  - ReDoc
