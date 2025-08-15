from django.core.cache import cache
from .models import Category, SpecialOffer

def categories(request):
    """
    Делает список всех категорий доступным во всех шаблонах.
    Результат кэшируется для уменьшения количества запросов к БД.
    """
    # Используем гранулярный ключ
    categories_cache_key = 'all_categories'
    cached_categories = cache.get(categories_cache_key)
    if cached_categories is None:
        categories_list = list(Category.objects.all())
        cache.set(categories_cache_key, categories_list, 60 * 60) # Кэш на 1 час
        return {'categories': categories_list}
    return {'categories': cached_categories}

def special_offer(request):
    """
    Делает активное спецпредложение доступным во всех шаблонах.
    """
    # Используем гранулярный ключ
    offer_cache_key = 'active_special_offer'
    cached_offer = cache.get(offer_cache_key)
    if cached_offer is None:
        offer = SpecialOffer.objects.get_active()
        cache.set(offer_cache_key, offer, 60 * 15) # Кэш на 15 минут
        return {'special_offer': offer}
    return {'special_offer': cached_offer}