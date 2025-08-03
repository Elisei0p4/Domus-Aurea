from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse

from store.factories import ProductFactory
from .wishlist import Wishlist

class WishlistTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product1 = ProductFactory(base_price=100)
        self.product2 = ProductFactory(base_price=200)

        self.session = self.client.session
        self.session[settings.WISH_SESSION_ID] = []
        self.session.save()

        # Create a mock request object to initialize the wishlist
        request = type('Request', (), {'session': self.session})()
        self.wishlist = Wishlist(request)

    def test_add_product(self):
        """Тестирует добавление товара и проверку дубликатов."""
        result1 = self.wishlist.add(self.product1)
        self.assertTrue(result1)
        self.assertIn(self.product1.id, self.wishlist.wishlist)
        self.assertEqual(len(self.wishlist), 1)

        result2 = self.wishlist.add(self.product1) # Повторное добавление
        self.assertFalse(result2)
        self.assertEqual(len(self.wishlist), 1)

    def test_remove_product(self):
        self.wishlist.add(self.product1)
        self.wishlist.add(self.product2)
        self.assertEqual(len(self.wishlist), 2)

        self.wishlist.remove(self.product1)
        self.assertNotIn(self.product1.id, self.wishlist.wishlist)
        self.assertIn(self.product2.id, self.wishlist.wishlist)
        self.assertEqual(len(self.wishlist), 1)

    def test_clear_wishlist(self):
        self.wishlist.add(self.product1)
        self.wishlist.clear()
        self.assertNotIn(settings.WISH_SESSION_ID, self.wishlist.session)

    def test_iteration(self):
        self.wishlist.add(self.product1)
        self.wishlist.add(self.product2)

        product_list = [p for p in self.wishlist]
        self.assertEqual(len(product_list), 2)
        self.assertIn(self.product1, product_list)
        self.assertIn(self.product2, product_list)

    def test_wishlist_view_ajax_add_remove(self):
        """Тестирует AJAX-добавление и удаление через представления."""
        # Добавление
        add_url = reverse('wishlist:wishlist_add', args=[self.product1.id])
        response_add = self.client.post(add_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response_add.status_code, 200)
        self.assertEqual(response_add.json()['status'], 'ok')
        self.assertEqual(response_add.json()['count'], 1)

        # Удаление
        remove_url = reverse('wishlist:wishlist_remove', args=[self.product1.id])
        response_remove = self.client.post(remove_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response_remove.status_code, 200)
        self.assertEqual(response_remove.json()['status'], 'ok')
        self.assertEqual(response_remove.json()['count'], 0)