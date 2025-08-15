from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Главные страницы магазина
    path('', views.home_view, name='home'),
    path('shop/', views.product_list_view, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list_view, name='product_list_by_category'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail'),

    # Новая ссылка для покупки в 1 клик
    path('buy-now/<int:product_id>/', views.buy_now_view, name='buy_now'),

    path('subscribe/', views.subscribe_view, name='subscribe'),

    # Реальные страницы вместо заглушек
    path('account/', views.account_view, name='account'),
    path('new-arrivals/', views.new_arrivals_view, name='new_arrivals'),
    path('sale/', views.sale_view, name='sale'),
    path('contacts/', views.contact_view, name='contacts'),
    path('about/', views.about_view, name='about'),

    # Универсальный роутер для простых статических страниц
    path('page/<slug:page_name>/', views.StaticPageView.as_view(), name='static_page'),
    
    # URL-заглушка, которая пока останется
    path('track-order/', views.StaticPageView.as_view(), {'page_name': 'track-order'}, name='track_order'),
]