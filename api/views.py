from rest_framework import viewsets, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404

from store.models import Product, Category, Review
from orders.models import Order
from cart.cart import Cart
from wishlist.wishlist import Wishlist
from comparison.comparison import Comparison

from .serializers import (
    ProductSerializer, CategorySerializer, ReviewSerializer,
    OrderSerializer, OrderCreateSerializer
)

class SearchSuggestAPIView(APIView):
    """
    API эндпоинт для получения поисковых подсказок в виде объектов.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response([])

        products = Product.objects.filter(
            name__icontains=query,
            available=True
        ).distinct()[:6]

        results = []
        for p in products:
            image_url = p.get_main_image_url()
            results.append({
                'name': p.name,
                'url': p.get_absolute_url(),
                'image_url': request.build_absolute_uri(image_url),
                'price': f'{p.final_price:,.0f}'.replace(',', ' '),
                'old_price': f'{p.old_price:,.0f}'.replace(',', ' ') if p.old_price else None,
            })

        return Response(results)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__slug', 'brand']
    ordering_fields = ['created', 'name', 'final_price']
    search_fields = ['name', 'description', 'brand']
    queryset = Product.objects.available().select_related('category').prefetch_related('reviews')

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.filter(is_active=True)
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get('product_id'))
        serializer.save(author=self.request.user, author_name=self.request.user.get_full_name() or self.request.user.username, product=product)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items', 'items__product')
    def get_serializer_class(self):
        if self.action == 'create': return OrderCreateSerializer
        return OrderSerializer


class UserActionAPIView(APIView):
    """
    Универсальный API View для действий пользователя (корзина, избранное, сравнение).
    Определяет действие и сущность на основе URL.
    Поддерживаемые URL:
    - /api/action/cart/add/
    - /api/action/cart/remove/
    - /api/action/wishlist/toggle/
    - /api/action/comparison/toggle/
    """
    permission_classes = [permissions.AllowAny]
    
    ACTION_MAP = {
        'cart': {
            'add': '_cart_add',
            'remove': '_cart_remove',
        },
        'wishlist': {
            'toggle': '_wishlist_toggle',
        },
        'comparison': {
            'toggle': '_comparison_toggle',
        }
    }

    def post(self, request, entity, action, *args, **kwargs):
        handler_method_name = self.ACTION_MAP.get(entity, {}).get(action)
        if not handler_method_name:
            raise Http404("Action not found")
        
        handler = getattr(self, handler_method_name, None)
        if not handler:
            raise Http404("Action handler not implemented")

        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id, available=True)
        
        return handler(request, product)

    def _cart_add(self, request, product):
        cart = Cart(request)
        try:
            quantity = int(request.data.get('quantity', 1))
            if quantity < 1: raise ValueError()
        except (ValueError, TypeError):
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
        
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock', 'stock': product.stock}, status=status.HTTP_400_BAD_REQUEST)

        cart.add(product=product, quantity=quantity)
        
        return Response({
            'status': 'ok', 
            'message': f'Товар "{product.name}" добавлен в корзину.',
            'cart_unique_items_count': len(cart),
            'cart_total_price': cart.get_total_price()
        }, status=status.HTTP_200_OK)

    def _cart_remove(self, request, product):
        cart = Cart(request)
        cart.remove(product)
        return Response({
            'status': 'ok',
            'message': f'Товар "{product.name}" удален из корзины.',
            'cart_unique_items_count': len(cart),
            'cart_total_price': cart.get_total_price()
        }, status=status.HTTP_200_OK)

    def _wishlist_toggle(self, request, product):
        wishlist = Wishlist(request)
        
        if product.id in wishlist.get_product_ids():
            wishlist.remove(product)
            action_result = 'removed'
            message = f'Товар "{product.name}" удален из избранного.'
        else:
            wishlist.add(product)
            action_result = 'added'
            message = f'Товар "{product.name}" добавлен в избранное.'

        return Response({
            'status': 'ok',
            'action': action_result,
            'message': message,
            'wishlist_count': len(wishlist)
        }, status=status.HTTP_200_OK)

    def _comparison_toggle(self, request, product):
        comparison = Comparison(request)
        
        if product.id in comparison.get_product_ids():
            comparison.remove(product)
            action_result = 'removed'
            message = f'Товар "{product.name}" убран из сравнения.'
        else:
            comparison.add(product)
            action_result = 'added'
            message = f'Товар "{product.name}" добавлен к сравнению.'

        return Response({
            'status': 'ok',
            'action': action_result,
            'message': message,
            'comparison_count': len(comparison)
        }, status=status.HTTP_200_OK)