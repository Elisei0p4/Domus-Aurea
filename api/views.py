# api/views.py

from rest_framework import viewsets, filters, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from store.models import Product, Category, Review
from orders.models import Order
from cart.cart import Cart
from wishlist.wishlist import Wishlist

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
            image_url = p.image.url if p.image else '/static/images/placeholder.png'
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

class CartItemAddAPIView(APIView):
    permission_classes = [permissions.AllowAny] 

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError()
        except (ValueError, TypeError):
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart.add(product=product, quantity=quantity)
        
        return Response({
            'status': 'ok', 
            'cart_count': len(cart), 
            'cart_total': cart.get_total_price()
        }, status=status.HTTP_200_OK)


class WishlistToggleAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist = Wishlist(request)
        product = get_object_or_404(Product, id=product_id)

        if product.id in wishlist.wishlist:
            wishlist.remove(product)
            action = 'removed'
        else:
            wishlist.add(product)
            action = 'added'
        
        return Response({
            'status': 'ok',
            'action': action,
            'wishlist_count': len(wishlist)
        }, status=status.HTTP_200_OK)