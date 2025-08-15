from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from store.factories import UserFactory, ProductFactory
from orders.models import Order
from store.models import Product
from decimal import Decimal

class OrderCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.force_login(self.user)

        self.product = ProductFactory(base_price=Decimal('150.00'), stock=10, discount=0)
        
        self.order_data = {
            'first_name': 'Тест',
            'last_name': 'Тестов',
            'email': 'test@example.com',
            'address': 'ул. Тестовая, 1',
            'postal_code': '123456',
            'city': 'Тест-сити'
        }
        self.create_url = reverse('orders:order_create')

    def test_order_creation_and_stock_decrease(self):
        """Тестирует успешное создание заказа и уменьшение остатков товара."""
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            str(self.product.id): {'quantity': 2, 'price': str(self.product.final_price)}
        }
        session.save()

        initial_stock = self.product.stock
        order_quantity = 2

        # Делаем POST-запрос и сразу следуем по редиректу
        response = self.client.post(self.create_url, self.order_data, follow=True)
        
        # 1. Проверяем, что нас перенаправило на нужную страницу
        self.assertRedirects(response, reverse('orders:created'), status_code=302, target_status_code=200)
        
        # 2. Проверяем состояние базы данных
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)
        
        product_after_order = Product.objects.get(id=self.product.id)
        self.assertEqual(product_after_order.stock, initial_stock - order_quantity)
        
        # 3. Проверяем, что на финальной странице есть нужный контент
        self.assertContains(response, f"Ваш заказ <span class=\"font-bold text-gray-800\">#{order.id}</span> успешно создан.")
        
        # 4. Проверяем, что сессия корзины была очищена
        session_after_order = self.client.session
        self.assertNotIn(settings.CART_SESSION_ID, session_after_order)
        # И сессия order_id тоже очищена (так как мы уже "посетили" страницу)
        self.assertNotIn('order_id', session_after_order)


    def test_order_creation_insufficient_stock(self):
        """Тестирует невозможность создания заказа при нехватке товара."""
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            str(self.product.id): {'quantity': 20, 'price': str(self.product.final_price)}
        }
        session.save()
        
        response = self.client.post(self.create_url, self.order_data, follow=True)

        self.assertEqual(Order.objects.count(), 0)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

        self.assertRedirects(response, reverse('cart:cart_detail'))
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn(f"Недостаточно товара '{self.product.name}'", str(messages[0]))

    def test_order_creation_with_empty_cart(self):
        """Тестирует редирект при попытке создать заказ с пустой корзиной."""
        session = self.client.session
        session[settings.CART_SESSION_ID] = {}
        session.save()
        
        response = self.client.get(self.create_url)
        self.assertRedirects(response, reverse('store:product_list'))