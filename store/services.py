from typing import Dict, Optional
from django.contrib.auth.models import User
from .models import Product, Review
from .forms import ReviewForm


def add_review(user: User, product: Product, data: Dict) -> Optional[Review]:
    """
    Сервисная функция для добавления отзыва к товару.
    1. Проверяет, аутентифицирован ли пользователь.
    2. Валидирует данные формы.
    3. Создает объект Review, связывая его с пользователем и товаром.
    Возвращает созданный объект Review или None в случае ошибки/невалидных данных.
    """
    if not user.is_authenticated:
        return None

    form = ReviewForm(data)
    if not form.is_valid():
        return None

    new_review = form.save(commit=False)
    new_review.product = product
    new_review.author = user
    new_review.author_name = user.get_full_name() or user.username
    new_review.save()
    
    return new_review