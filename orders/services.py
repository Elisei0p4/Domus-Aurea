# orders/services.py

from typing import Dict, Optional
from django.contrib.auth.models import User
from django.db import transaction
from cart.cart import Cart
from store.models import Product
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created_email


@transaction.atomic
def create_order(cart: Cart, form_data: Dict, user: Optional[User] = None) -> Optional[Order]:
    """
    Сервисная функция для создания заказа.
    1. Валидирует данные формы.
    2. Создает объект Order.
    3. Переносит товары из корзины в OrderItem, проверяя и уменьшая остатки.
    4. Очищает корзину.
    5. Запускает асинхронную задачу отправки email.
    
    Эта функция должна вызываться внутри блока transaction.atomic().
    В случае нехватки товара вызывает ValueError.
    """
    form = OrderCreateForm(form_data)
    if not form.is_valid():
        return None

    order = form.save(commit=False)
    if user and user.is_authenticated:
        order.user = user
    order.save()

    product_ids = [item['product'].id for item in cart]
    products = Product.objects.select_for_update().filter(id__in=product_ids)
    product_map = {product.id: product for product in products}

    for item in cart:
        product = product_map.get(item['product'].id)
        if product.stock < item['quantity']:
            raise ValueError(f"Недостаточно товара '{product.name}' на складе. Доступно: {product.stock} шт.")
        
        OrderItem.objects.create(
            order=order,
            product=product,
            price=item['price'],
            quantity=item['quantity']
        )
        product.stock -= item['quantity']
        # Увеличиваем счетчик покупок
        product.purchase_count += item['quantity']
    
    Product.objects.bulk_update(products, ['stock', 'purchase_count'])
    
    cart.clear()
    
    order_created_email.delay(order.id)
    
    return order