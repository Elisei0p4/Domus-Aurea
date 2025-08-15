from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('tag/<slug:tag_slug>/', views.article_list, name='article_list_by_tag'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('<int:article_id>/comment/', views.post_comment, name='post_comment'),
]