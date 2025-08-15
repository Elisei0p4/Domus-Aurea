from .cart import Cart
from wishlist.wishlist import Wishlist

def cart(request):
    cart_instance = Cart(request)
    wishlist_instance = Wishlist(request)
    
    cart_json_data = {
        'items': [
            {
                'product': {
                    'id': item['product'].id,
                    'name': item['product'].name,
                    'url': item['product'].get_absolute_url(),
                    'image_url': item['product'].get_main_image_url(),
                    'category_name': item['product'].category.name,
                    'stock': item['product'].stock,
                },
                'quantity': item['quantity'],
                'price': str(item['price']),
                'total_price': str(item['total_price']),
            } for item in cart_instance
        ],
        'total_quantity': cart_instance.get_total_quantity(),
        'subtotal': str(cart_instance.get_total_price()),
        'discount': str(cart_instance.get_discount()),
        'total': str(cart_instance.get_total_price_after_discount()),
        'promo_code': {
            'code': cart_instance.promo_code.code,
            'discount_percent': cart_instance.promo_code.discount_percent
        } if cart_instance.promo_code else None,
        'wishlist_ids': wishlist_instance.get_product_ids()
    }
    
    
    return {
        'cart': cart_instance,
        'cart_json_data': cart_json_data
    }