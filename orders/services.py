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
    2. Создает объект Order, применяет скидку по промокоду.
    3. Блокирует строки товаров для безопасного списания остатков.
    4. Переносит товары из корзины в OrderItem, проверяя и уменьшая остатки.
    5. Очищает корзину.
    6. Запускает асинхронную задачу отправки email.
    
    В случае нехватки товара вызывает ValueError.
    """
    form = OrderCreateForm(form_data)
    if not form.is_valid():
        return None

    order = form.save(commit=False)
    if user and user.is_authenticated:
        order.user = user
    
    # Применяем промокод из корзины
    if cart.promo_code:
        order.promo_code = cart.promo_code
        order.discount = cart.get_discount()

    order.save()

    product_ids = [item['product'].id for item in cart]
    # Блокируем строки товаров для безопасного обновления
    products = Product.objects.select_for_update().filter(id__in=product_ids)
    product_map = {product.id: product for product in products}

    for item in cart:
        product = product_map.get(item['product'].id)
        if product.stock < item['quantity']:
            # Транзакция будет отменена автоматически при возникновении исключения
            raise ValueError(f"Недостаточно товара '{product.name}' на складе. Доступно: {product.stock} шт.")
        
        OrderItem.objects.create(
            order=order,
            product=product,
            price=item['price'],
            quantity=item['quantity']
        )
        product.stock -= item['quantity']
        product.purchase_count += item['quantity']
    
    # Сохраняем обновленные остатки и счетчики покупок одним запросом
    Product.objects.bulk_update(products, ['stock', 'purchase_count'])
    
    cart.clear()
    
    order_created_email.delay(order.id)
    
    return order