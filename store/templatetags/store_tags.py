from django import template
from django.conf import settings
from store.models import Product

register = template.Library()

@register.inclusion_tag('store/partials/bestsellers_list.html')
def get_bestsellers(count=4):
    """
    Получает самые продаваемые товары.
    """
    bestsellers = Product.objects.available().order_by('-purchase_count')[:count]
    return {'bestsellers': bestsellers}

@register.inclusion_tag('store/partials/recently_viewed_list.html')
def get_recently_viewed(request, count=5):
    """
    Получает недавно просмотренные товары из сессии.
    """
    recently_viewed_ids = request.session.get(settings.RECENTLY_VIEWED_SESSION_ID, [])
    
    if not recently_viewed_ids:
        return {'recently_viewed_products': []}
        

    products = Product.objects.available().filter(id__in=recently_viewed_ids)
    

    product_map = {p.id: p for p in products}
    ordered_products = [product_map[pid] for pid in recently_viewed_ids if pid in product_map][:count]
    
    return {'recently_viewed_products': ordered_products}