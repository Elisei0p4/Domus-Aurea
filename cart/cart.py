# cart/cart.py

from decimal import Decimal
from django.conf import settings
from store.models import Product
import copy

class Cart:
    def __init__(self, request):
        """
        Инициализация корзины.
        Теперь __init__ только загружает корзину из сессии, но не создает ее.
        """
        self.session = request.session
        # self.cart теперь может быть None, если корзины в сессии нет
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            # Если корзины нет в сессии, инициализируем ее как пустой словарь
            self.cart = {}
            
        # Поле для кеширования объектов Product
        self.products_cache = None

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        Теперь этот метод отвечает за создание корзины в сессии, если ее не было.
        """
        product_id = str(product.id)
        
        # Если корзина была создана только в __init__ (как пустой dict),
        # но еще не в сессии, мы создаем ключ в сессии здесь.
        if settings.CART_SESSION_ID not in self.session:
            self.session[settings.CART_SESSION_ID] = self.cart

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.final_price)}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Убеждаемся, что сессия будет сохранена
        self.session.modified = True
        # Сбрасываем кеш при любом изменении корзины
        self.products_cache = None

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        if self.products_cache is None:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            # Сохраняем их в кеш
            self.products_cache = {str(p.id): p for p in products}

        cart = copy.deepcopy(self.cart) 
        
        for product_id, item in cart.items():
            product = self.products_cache.get(product_id)
            if product:
                item['product'] = product
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Подсчет УНИКАЛЬНЫХ товарных позиций в корзине.
        """
        return len(self.cart.keys())

    def get_total_quantity(self):
        """
        Подсчет ОБЩЕГО количества всех единиц товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости всех товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Полное удаление корзины из сессии.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True