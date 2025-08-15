from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from store.factories import CategoryFactory, ProductFactory, UserFactory, ReviewFactory
from store.models import Product, Category, Review

class ProductAPITests(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.product1 = ProductFactory(category=self.category, name="Тестовый диван", final_price=50000)
        self.product2 = ProductFactory(name="Тестовое кресло", final_price=20000)
        ProductFactory(available=False) # Недоступный товар
    
    def test_list_products(self):
        """Проверяет получение списка доступных товаров."""
        url = reverse('api:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) # Только доступные
        self.assertEqual(response.data['results'][0]['name'], self.product2.name) # По умолчанию сортировка по -created
        
    def test_filter_products_by_category(self):
        """Проверяет фильтрацию товаров по слагу категории."""
        url = reverse('api:product-list') + f'?category__slug={self.category.slug}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.product1.name)

    def test_search_products(self):
        """Проверяет поиск по названию."""
        url = reverse('api:product-list') + '?search=диван'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.product1.id)

    def test_retrieve_product(self):
        """Проверяет получение одного товара по ID."""
        url = reverse('api:product-detail', kwargs={'pk': self.product1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

class ReviewAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.review = ReviewFactory(product=self.product, author=self.user, is_active=True)
        ReviewFactory(product=self.product, is_active=False) # Неактивный отзыв
    
    def test_list_reviews_for_product(self):
        """Проверяет получение списка активных отзывов для товара."""
        url = reverse('api:review-list') + f'?product_id={self.product.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) # Только активные
        self.assertEqual(response.data['results'][0]['id'], self.review.id)
        
    def test_create_review_unauthenticated(self):
        """Проверяет, что неавторизованный пользователь не может создать отзыв."""
        url = reverse('api:review-list')
        data = {'product_id': self.product.id, 'text': 'Новый отзыв', 'rating': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_review_authenticated(self):
        """Проверяет создание отзыва авторизованным пользователем."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:review-list')
        data = {'product_id': self.product.id, 'text': 'Новый отзыв', 'rating': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)
        self.assertEqual(response.data['text'], 'Новый отзыв')
        self.assertEqual(response.data['author_name'], self.user.get_full_name())

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product1 = ProductFactory(stock=10, final_price=100)
        self.product2 = ProductFactory(stock=5, final_price=200)
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        """Проверяет успешное создание заказа через API."""
        url = reverse('api:order-list')
        order_data = {
            "first_name": "API", "last_name": "User", "email": "api@test.com",
            "address": "API Street 1", "postal_code": "12345", "city": "APItown",
            "items": [
                {"product_id": self.product1.id, "quantity": 2},
                {"product_id": self.product2.id, "quantity": 1}
            ]
        }
        response = self.client.post(url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        
        self.assertEqual(self.product1.stock, 8)
        self.assertEqual(self.product2.stock, 4)
        
        # Проверяем, что вернулся сериализатор для чтения
        self.assertIn('total_cost', response.data)
        self.assertEqual(response.data['total_cost'], '400.00')

    def test_create_order_insufficient_stock(self):
        """Проверяет ошибку при создании заказа с недостаточным количеством товара."""
        url = reverse('api:order-list')
        order_data = {
            "first_name": "API", "last_name": "User", "email": "api@test.com",
            "address": "API Street 1", "postal_code": "12345", "city": "APItown",
            "items": [{"product_id": self.product1.id, "quantity": 11}]
        }
        response = self.client.post(url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(f"Недостаточно товара '{self.product1.name}' на складе.", str(response.data))

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 10) # Остаток не изменился