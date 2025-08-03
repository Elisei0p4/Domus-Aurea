# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'  # <--- ДОБАВИТЬ ЭТУ СТРОКУ

# Создаем router и регистрируем наши viewsets
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'orders', views.OrderViewSet, basename='order')

# URL-адреса API определяются автоматически роутером
urlpatterns = [
    path('', include(router.urls)),
    path('search-suggest/', views.SearchSuggestAPIView.as_view(), name='search-suggest'),
    
    # НОВЫЕ URL для интерактивных действий
    path('cart/add/', views.CartItemAddAPIView.as_view(), name='api-cart-add'),
    path('wishlist/toggle/', views.WishlistToggleAPIView.as_view(), name='api-wishlist-toggle'),
]