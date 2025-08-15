from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Review
from .factories import ProductFactory, UserFactory, ReviewFactory, CategoryFactory
from decimal import Decimal

# --- Тесты Моделей ---
class StoreModelTests(TestCase):

    def setUp(self):
        self.product_no_discount = ProductFactory(base_price=Decimal('1000.00'), discount=0)
        self.product_with_discount = ProductFactory(base_price=Decimal('2000.00'), discount=25)
        self.product_unavailable = ProductFactory(stock=0, available=False)

    def test_product_price_property(self):
        """Тестирует свойство 'price' для товаров со скидкой и без."""
        # Сверяемся с итоговой ценой, которая рассчитывается в save()
        self.assertEqual(self.product_no_discount.final_price, Decimal('1000.00'))
        self.assertEqual(self.product_with_discount.final_price, Decimal('1500.00'))

    def test_product_old_price_property(self):
        """Тестирует свойство 'old_price'."""
        self.assertIsNone(self.product_no_discount.old_price)
        self.assertEqual(self.product_with_discount.old_price, Decimal('2000.00'))

    def test_product_manager_available(self):
        """Тестирует менеджер на доступные товары."""
        self.assertEqual(Product.objects.available().count(), 2)
        self.assertIn(self.product_no_discount, Product.objects.available())
        self.assertNotIn(self.product_unavailable, Product.objects.available())

    def test_product_manager_on_sale(self):
        """Тестирует менеджер на товары со скидкой."""
        self.assertEqual(Product.objects.on_sale().count(), 1)
        self.assertIn(self.product_with_discount, Product.objects.on_sale())
        self.assertNotIn(self.product_no_discount, Product.objects.on_sale())

    def test_product_review_aggregation(self):
        """Тестирует подсчет среднего рейтинга и количества отзывов."""
        ReviewFactory(product=self.product_no_discount, rating=5, is_active=True)
        ReviewFactory(product=self.product_no_discount, rating=3, is_active=True)
        ReviewFactory(product=self.product_no_discount, rating=4, is_active=False) # Inactive

        self.product_no_discount.refresh_from_db()
        self.assertEqual(self.product_no_discount.review_count, 2)
        self.assertEqual(self.product_no_discount.average_rating, 4.0)


# --- Тесты Представлений (Views) ---
class StoreViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.category = CategoryFactory(name='Категория для вью', slug='view-category')
        self.product = ProductFactory(category=self.category, name='Тестовый товар', slug='view-product', available=True)

    def test_home_view(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')

    def test_product_list_view(self):
        """Тестирует базовый вид списка товаров."""
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_list_by_category_view(self):
        """Тестирует фильтрацию по категории."""
        other_product = ProductFactory(name='Другой товар', available=True)
        
        url = reverse('store:product_list_by_category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, other_product.name)

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertTemplateUsed(response, 'store/product_detail.html')

    def test_product_list_filtering_and_sorting(self):
        """Тестирует фильтрацию по цене и сортировку."""
        ProductFactory(name='Дешевый', base_price=Decimal('100.00'), discount=0, available=True)
        ProductFactory(name='Дорогой', base_price=Decimal('1000.00'), discount=0, available=True)
        
        # Фильтр по мин. цене
        response = self.client.get(reverse('store:product_list') + '?min_price=600')
        self.assertNotContains(response, 'Дешевый')
        self.assertContains(response, 'Дорогой')
        
        # Сортировка по возрастанию цены
        response = self.client.get(reverse('store:product_list') + '?ordering=final_price')
        products = list(response.context['products'])
        
        prices = [p.final_price for p in products]
        self.assertEqual(prices, sorted(prices))

    def test_ajax_search_view(self):
        """Тестирует, что API эндпоинт для подсказок возвращает корректный JSON."""
        url = reverse('api:search-suggest') + '?q=Тестовый'
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], self.product.name)

    def test_review_submission_authenticated(self):
        """Тестирует отправку отзыва аутентифицированным пользователем."""
        self.client.force_login(self.user)
        self.assertEqual(self.product.reviews.count(), 0)
        
        post_data = {'rating': 5, 'text': 'Очень хороший товар!', 'submit_review': '1'}
        response = self.client.post(self.product.get_absolute_url(), post_data, follow=True)
        
        self.assertRedirects(response, self.product.get_absolute_url())
        self.assertEqual(self.product.reviews.count(), 1)
        review = self.product.reviews.first()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.author, self.user)
        self.assertContains(response, "Спасибо за ваш отзыв!")

    def test_review_submission_unauthenticated(self):
        """Тестирует невозможность отправки отзыва неаутентифицированным пользователем."""
        self.assertEqual(self.product.reviews.count(), 0)
        post_data = {'rating': 5, 'text': 'Плохой отзыв от анонима', 'submit_review': '1'}
        response = self.client.post(self.product.get_absolute_url(), post_data)
        

        self.assertEqual(self.product.reviews.count(), 0)

        self.assertContains(response, "Пожалуйста, <a href=")