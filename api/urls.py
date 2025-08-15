from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'orders', views.OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
    path('search-suggest/', views.SearchSuggestAPIView.as_view(), name='search-suggest'),
    path('action/<str:entity>/<str:action>/', views.UserActionAPIView.as_view(), name='user-action'),
]