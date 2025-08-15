from django.contrib import admin
from .models import Article, Tag, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published', 'is_featured', 'views')
    list_filter = ('is_published', 'is_featured', 'created_at', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)
    list_editable = ('is_published', 'is_featured')
    readonly_fields = ('views',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'body', 'article', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author_name', 'email', 'body')
    list_editable = ('is_active',)