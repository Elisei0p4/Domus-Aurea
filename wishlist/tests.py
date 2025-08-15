from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse

from store.factories import ProductFactory
from .wishlist import Wishlist

class WishlistTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product1 = ProductFactory(base_price=100, available=True)
        self.product2 = ProductFactory(base_price=200, available=True)

        self.session = self.client.session
        self.session[settings.WISH_SESSION_ID] = []
        self.session.save()

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

    def test_wishlist_ajax_toggle_via_api(self):
        """Тестирует AJAX-добавление и удаление через универсальный API."""
        url = reverse('api:user-action', kwargs={'entity': 'wishlist', 'action': 'toggle'})
        post_data = {'product_id': self.product1.id}

        # Добавление
        response_add = self.client.post(url, data=post_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response_add.status_code, 200)
        json_add = response_add.json()
        self.assertEqual(json_add['status'], 'ok')
        self.assertEqual(json_add['action'], 'added')
        self.assertEqual(json_add['wishlist_count'], 1)

        # Удаление
        response_remove = self.client.post(url, data=post_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response_remove.status_code, 200)
        json_remove = response_remove.json()
        self.assertEqual(json_remove['status'], 'ok')
        self.assertEqual(json_remove['action'], 'removed')
        self.assertEqual(json_remove['wishlist_count'], 0)