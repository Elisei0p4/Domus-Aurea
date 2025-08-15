from decimal import Decimal
from django.conf import settings
from store.models import Product
from orders.models import PromoCode
import copy

class Cart:
    def __init__(self, request):
        """
        Инициализация корзины и промокода.
        """
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            self.cart = self.session[settings.CART_SESSION_ID] = {}
        
        # Логика промокода
        self.promo_code_id = self.session.get('promo_code_id')
        self.products_cache = None

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.final_price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
                self.save()
            else:
                self.remove(product)

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session['promo_code_id'] = self.promo_code_id
        self.session.modified = True
        self.products_cache = None

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        if self.products_cache is None:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids).select_related('category')
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
        return len(self.cart.keys())

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        if 'promo_code_id' in self.session:
            del self.session['promo_code_id']
        self.session.modified = True

    # --- Методы для промокода ---
    
    @property
    def promo_code(self):
        if self.promo_code_id:
            try:
                return PromoCode.objects.get(id=self.promo_code_id)
            except PromoCode.DoesNotExist:
                return None
        return None

    def get_discount(self):
        if self.promo_code:
            discount_percent = self.promo_code.discount_percent
            return (self.get_total_price() * Decimal(discount_percent / 100)).quantize(Decimal('0.01'))
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
        
    def apply_promo_code(self, promo_code_obj):
        self.promo_code_id = promo_code_obj.id
        self.save()
    
    def remove_promo_code(self):
        self.promo_code_id = None
        self.save()