from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('promo/apply/', views.promo_code_apply, name='promo_code_apply'),
    path('promo/remove/', views.promo_code_remove, name='promo_code_remove'),
]