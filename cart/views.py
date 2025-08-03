from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.urls import reverse
import json

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok',
                'cart_total': f'{cart.get_total_price():,.0f}'.replace(',', ' '),
                'cart_count': len(cart),
                'product_name': product.name,
            })
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_total': f'{cart.get_total_price():,.0f}'.replace(',', ' '),
            'cart_count': len(cart),
            'product_name': product.name,
        })
    
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    cart_items_list = list(cart)

    cart_items_for_js = []
    for item in cart_items_list:
        product = item['product']
        cart_items_for_js.append({
            'id': product.id,
            'name': product.name,
            'imageUrl': product.image.url if product.image else '',
            'productUrl': product.get_absolute_url(),
            'quantity': item['quantity'],
            'price': float(item['price']),
            'removeUrl': reverse('cart:cart_remove', args=[product.id]),
        })
        
    context = {
        'cart': cart,
        'cart_items_json': json.dumps(cart_items_for_js)
    }
    return render(request, 'cart/detail.html', context)