from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse
from store.factories import ProductFactory
from .cart import Cart
from decimal import Decimal

class CartTests(TestCase):

    def setUp(self):
        self.product1 = ProductFactory(name='Товар 1', base_price=Decimal('100.00'), discount=0, available=True)
        self.product2 = ProductFactory(name='Товар 2', base_price=Decimal('200.00'), discount=0, available=True)
        
        self.client = Client()
        self.session = self.client.session
        self.session[settings.CART_SESSION_ID] = {}
        self.session.save()
        
        request = type('Request', (), {'session': self.session})()
        self.cart = Cart(request)

    def test_add_product(self):
        self.cart.add(product=self.product1, quantity=2)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_quantity(), 2)
        self.assertIn(str(self.product1.id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 2)

    def test_add_same_product_increments_quantity(self):
        self.cart.add(product=self.product1, quantity=1)
        self.cart.add(product=self.product1, quantity=2)
        self.assertEqual(self.cart.get_total_quantity(), 3)
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 3)
        
    def test_update_quantity(self):
        self.cart.add(product=self.product1, quantity=1)
        self.cart.update(product=self.product1, quantity=5)
        self.assertEqual(self.cart.get_total_quantity(), 5)
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 5)

    def test_remove_product(self):
        self.cart.add(product=self.product1)
        self.cart.remove(self.product1)
        self.assertEqual(self.cart.get_total_quantity(), 0)
        self.assertNotIn(str(self.product1.id), self.cart.cart)

    def test_get_total_price(self):
        self.cart.add(product=self.product1, quantity=2)
        self.cart.add(product=self.product2, quantity=1)
        self.assertEqual(self.cart.get_total_price(), Decimal('400.00'))

    def test_clear_cart(self):
        self.cart.add(product=self.product1)
        self.cart.clear()
        self.assertNotIn(settings.CART_SESSION_ID, self.cart.session)

    def test_cart_view_ajax_add_via_api(self):
        """
        Тестирует AJAX-добавление товара в корзину через новый универсальный API.
        """
        url = reverse('api:user-action', kwargs={'entity': 'cart', 'action': 'add'})
        
        post_data = {
            'product_id': self.product1.id,
            'quantity': 2,
        }
        
        response = self.client.post(
            url,
            data=post_data,
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['cart_total_quantity'], 2)