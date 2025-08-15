from django.urls import path
from . import views

app_name = 'comparison'

urlpatterns = [
    path('', views.comparison_detail, name='comparison_detail'),
    path('clear/', views.comparison_clear, name='comparison_clear'),
]