from django.core.cache import cache
from .models import Category, SpecialOffer

def categories(request):
    """
    Делает список всех категорий доступным во всех шаблонах.
    Результат кэшируется для уменьшения количества запросов к БД.
    """
    categories_cache_key = 'all_categories'
    cached_categories = cache.get(categories_cache_key)
    if cached_categories is None:
        categories_list = Category.objects.all()
        cache.set(categories_cache_key, list(categories_list), 60 * 60) # Кэш на 1 час
        return {'categories': categories_list}
    return {'categories': cached_categories}

# НОВЫЙ КОНТЕКСТ-ПРОЦЕССОР
def special_offer(request):
    """
    Делает активное спецпредложение доступным во всех шаблонах.
    """
    offer = SpecialOffer.objects.get_active()
    return {'special_offer': offer}