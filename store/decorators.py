from functools import wraps
from django.conf import settings
from .models import Product

MAX_RECENTLY_VIEWED = 5

def track_viewed_product(view_func):
    """
    Декоратор для отслеживания просмотренных товаров.
    Сохраняет ID товара в сессии пользователя.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        product_slug = kwargs.get('product_slug')
        if product_slug:
            try:
                product_id = Product.objects.values_list('id', flat=True).get(slug=product_slug, available=True)
                
                # Получаем текущий список из сессии
                recently_viewed_ids = request.session.get(settings.RECENTLY_VIEWED_SESSION_ID, [])
                
                # Если товар уже есть в списке, удаляем его, чтобы переместить наверх
                if product_id in recently_viewed_ids:
                    recently_viewed_ids.remove(product_id)
                
                # Добавляем товар в начало списка
                recently_viewed_ids.insert(0, product_id)
                
                # Ограничиваем список до MAX_RECENTLY_VIEWED товаров
                if len(recently_viewed_ids) > MAX_RECENTLY_VIEWED:
                    recently_viewed_ids = recently_viewed_ids[:MAX_RECENTLY_VIEWED]
                
                # Сохраняем обновленный список в сессию
                request.session[settings.RECENTLY_VIEWED_SESSION_ID] = recently_viewed_ids
            
            except Product.DoesNotExist:
                # Если товар не найден, ничего не делаем
                pass
        
        # Вызываем оригинальную view-функцию
        return view_func(request, *args, **kwargs)
        
    return wrapper