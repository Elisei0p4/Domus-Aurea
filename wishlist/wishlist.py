from django.conf import settings
from store.models import Product

class Wishlist:
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(settings.WISH_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISH_SESSION_ID] = []
        self.wishlist = wishlist
        self.products_cache = None

    def add(self, product):
        product_id = product.id
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
            self.save()
            return True
        return False

    def remove(self, product):
        product_id = product.id
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            self.save()

    def __iter__(self):
        if self.products_cache is None:
            product_ids = self.get_product_ids()
            products = Product.objects.filter(id__in=product_ids)
            self.products_cache = list(products)

        for product in self.products_cache:
            yield product

    def __len__(self):
        return len(self.wishlist)
    
    def get_product_ids(self):
        return self.wishlist

    def clear(self):
        if settings.WISH_SESSION_ID in self.session:
            del self.session[settings.WISH_SESSION_ID]
            self.save()

    def save(self):
        self.session.modified = True
        self.products_cache = None