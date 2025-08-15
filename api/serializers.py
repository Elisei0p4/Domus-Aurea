from rest_framework import serializers, exceptions
from django.db import transaction
from django.shortcuts import get_object_or_404

from store.models import Category, Product, Review
from orders.models import Order, OrderItem
from orders.tasks import order_created_email


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категорий."""
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'url']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзывов."""
    author_name = serializers.CharField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'author_name', 'text', 'rating', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Продуктов."""
    category = CategorySerializer(read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    old_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'url', 'category', 'image', 'model_3d',
            'description', 'average_rating', 'review_count', 'brand',
            'characteristics', 'sku', 'base_price', 'discount', 'final_price',
            'old_price', 'stock', 'available'
        ]

# --- Сериализаторы для ЗАПИСИ (создания) заказа ---
class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            
            for item_data in items_data:
                product = get_object_or_404(Product, id=item_data['product_id'])
                if product.stock < item_data['quantity']:
                    raise exceptions.ValidationError(f"Недостаточно товара '{product.name}' на складе.")

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.final_price, 
                    quantity=item_data['quantity']
                )
                product.stock -= item_data['quantity']
                product.save(update_fields=['stock'])
        
        order_created_email.delay(order.id)
        
        return order

# --- Сериализаторы для ЧТЕНИЯ заказа ---
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(source='get_total_cost', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
            'city', 'created', 'paid', 'items', 'total_cost'
        ]