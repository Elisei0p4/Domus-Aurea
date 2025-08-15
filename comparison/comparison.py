from django.conf import settings
from store.models import Product

class Comparison:
    """
    Класс для управления списком сравнения товаров в сессии.
    """
    def __init__(self, request):
        self.session = request.session
        comparison = self.session.get(settings.COMPARISON_SESSION_ID)
        if not comparison:
            comparison = self.session[settings.COMPARISON_SESSION_ID] = []
        self.comparison = comparison
        self.products_cache = None

    def add(self, product):
        """
        Добавляет товар в список сравнения, если его там нет.
        """
        product_id = product.id
        if product_id not in self.comparison:
            self.comparison.append(product_id)
            self.save()
            return True
        return False

    def remove(self, product):
        """
        Удаляет товар из списка сравнения.
        """
        product_id = product.id
        if product_id in self.comparison:
            self.comparison.remove(product_id)
            self.save()

    def __iter__(self):
        """
        Позволяет итерироваться по объектам Product в списке сравнения.
        Кэширует результат для эффективности.
        """
        if self.products_cache is None:
            product_ids = self.get_product_ids()
            # Используем prefetch_related для оптимизации доступа к характеристикам
            products = Product.objects.filter(id__in=product_ids).prefetch_related('category')
            # Сохраняем порядок, заданный в сессии
            product_map = {p.id: p for p in products}
            self.products_cache = [product_map[pid] for pid in product_ids if pid in product_map]
        
        for product in self.products_cache:
            yield product

    def __len__(self):
        """
        Возвращает количество товаров в списке сравнения.
        """
        return len(self.comparison)
    
    def get_product_ids(self):
        """
        Возвращает список ID товаров в списке сравнения.
        """
        return self.comparison

    def clear(self):
        """
        Полностью очищает список сравнения из сессии.
        """
        if settings.COMPARISON_SESSION_ID in self.session:
            del self.session[settings.COMPARISON_SESSION_ID]
            self.save()

    def save(self):
        """
        Сохраняет изменения в сессии.
        """
        self.session.modified = True
        self.products_cache = None