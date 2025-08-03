# store/admin.py

from django.contrib import admin
from .models import Category, Product, Review, Subscriber, ContactMessage, Feature, Slide, SpecialOffer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured']
    list_editable = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order')
    list_editable = ('display_order',)

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    list_display_links = ('alt_text',)

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'start_date', 'end_date')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'final_price', 'stock', 'available', 'is_featured']
    # ИСПРАВЛЕНО: 'final_price' удалено из списка редактируемых полей
    list_editable = ['is_featured', 'brand', 'stock', 'available']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'brand', 'collection', 'image', 'model_3d', 'description')
        }),
        ('Ценообразование и склад', {
            'fields': ('sku', 'base_price', 'discount', 'final_price', 'stock', 'available')
        }),
        ('Характеристики (JSON)', {
            'classes': ('collapse',),
            'fields': ('characteristics',)
        }),
        ('Продвижение', {
            'fields': ('is_featured',)
        }),
    )
    readonly_fields = ['final_price']
    list_filter = ['created', 'category', 'is_featured', 'brand', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'brand', 'collection', 'sku']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'author_name', 'rating', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'rating']
    list_editable = ['is_active']
    search_fields = ['author_name', 'text', 'product__name']

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    list_editable = ('is_processed',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')