# store/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category, Slide, Feature

def clear_full_site_cache(sender, instance, **kwargs):
    """
    Универсальная функция для полной очистки кэша сайта.
    Вызывается при изменении любой из ключевых моделей.
    """
    print(f"Сигнал от {sender.__name__} '{instance}': Очистка всего кэша.")
    cache.clear()

# Привязываем одну функцию к разным моделям для простоты
post_save.connect(clear_full_site_cache, sender=Product)
post_delete.connect(clear_full_site_cache, sender=Product)

post_save.connect(clear_full_site_cache, sender=Category)
post_delete.connect(clear_full_site_cache, sender=Category)

# НОВЫЕ СИГНАЛЫ ДЛЯ СЛАЙДОВ И ПРЕИМУЩЕСТВ
post_save.connect(clear_full_site_cache, sender=Slide)
post_delete.connect(clear_full_site_cache, sender=Slide)

post_save.connect(clear_full_site_cache, sender=Feature)
post_delete.connect(clear_full_site_cache, sender=Feature)