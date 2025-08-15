from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review, Subscriber, ContactMessage, Feature, Slide, SpecialOffer, ProductImage

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

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_thumbnail_display',)

    def image_thumbnail_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image_thumbnail.url)
        return "Нет изображения"
    image_thumbnail_display.short_description = "Миниатюра"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'category', 'brand', 'final_price', 'stock', 'available', 'is_featured']
    list_editable = ['is_featured', 'brand', 'stock', 'available']
    list_display_links = ['name']
    list_per_page = 20
    
    inlines = [ProductImageInline]

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
    readonly_fields = ['final_price', 'image_tag']
    list_filter = ['created', 'category', 'is_featured', 'brand', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'brand', 'collection', 'sku', 'category__name']
    search_help_text = 'Поиск по названию, описанию, бренду, артикулу и категории.'

    @admin.display(description='Изображение')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 70px; max-height: 70px;" />', obj.image.url)
        return "Нет фото"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'author_name', 'rating', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'rating']
    list_editable = ['is_active']
    search_fields = ['author_name', 'text', 'product__name']
    autocomplete_fields = ['product']

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