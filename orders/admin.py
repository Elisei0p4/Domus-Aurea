from django.contrib import admin
from .models import Order, OrderItem, PromoCode

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'price', 'quantity']
    readonly_fields = ['product', 'price', 'quantity']
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'created', 'promo_code']
    list_filter = ['paid', 'created', 'updated', 'promo_code']
    inlines = [OrderItemInline]
    readonly_fields = ['discount']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
    list_editable = ['is_active']