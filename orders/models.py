from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

from store.models import Product
from django.urls import reverse

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    valid_from = models.DateTimeField(verbose_name="Действителен с")
    valid_to = models.DateTimeField(verbose_name="Действителен до")
    discount_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Скидка в процентах"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ['-valid_from']

    def __str__(self):
        return self.code

    def clean(self):
        if self.valid_from >= self.valid_to:
            raise ValidationError("Дата начала действия не может быть позже или равна дате окончания.")

    @staticmethod
    def get_valid_promo(code_text):
        now = timezone.now()
        try:
            return PromoCode.objects.get(
                code__iexact=code_text,
                is_active=True,
                valid_from__lte=now,
                valid_to__gte=now
            )
        except PromoCode.DoesNotExist:
            return None


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    city = models.CharField(max_length=100, verbose_name="Город")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    paid = models.BooleanField(default=False, verbose_name="Оплачен")

    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Промокод")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Скидка по промокоду (сумма)")


    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id}'

    def get_subtotal_cost(self):
        """Возвращает стоимость товаров до скидки."""
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost(self):
        """Возвращает итоговую стоимость с учетом скидки."""
        subtotal = self.get_subtotal_cost()
        return subtotal - self.discount
    
    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity