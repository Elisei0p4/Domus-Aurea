from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib import messages
from store.models import Product
from orders.models import PromoCode
from .cart import Cart
from .forms import PromoCodeForm
from django.urls import reverse
import json

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))

        # Проверяем, что количество не превышает остаток на складе
        if quantity > product.stock:
            return JsonResponse({
                'status': 'error', 
                'error': f'На складе всего {product.stock} шт.'
            }, status=400)
            
        if quantity < 0:
            return JsonResponse({'status': 'error', 'error': 'Invalid quantity'}, status=400)
        
        cart.update(product=product, quantity=quantity)
        
        # Возвращаем расширенный ответ для обновления UI
        return JsonResponse({
            'status': 'ok',
            'cart_unique_items_count': len(cart),
            'cart_total_quantity': cart.get_total_quantity(),
            'cart_total_price': cart.get_total_price(),
            'cart_discount': cart.get_discount(),
            'cart_total_price_after_discount': cart.get_total_price_after_discount(),
            'item_total_price': product.final_price * quantity
        })
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    return JsonResponse({
        'status': 'ok',
        'product_name': product.name,
        'cart_unique_items_count': len(cart),
        'cart_total_price': cart.get_total_price(),
        'cart_discount': cart.get_discount(),
        'cart_total_price_after_discount': cart.get_total_price_after_discount(),
    })

def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    promo_form = PromoCodeForm()

    context = {
        'cart': cart,
        'promo_form': promo_form,
    }
    return render(request, 'cart/detail.html', context)


@require_POST
def promo_code_apply(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    form = PromoCodeForm(request.POST)
    if form.is_valid():
        code_text = form.cleaned_data['code']
        promo_code = PromoCode.get_valid_promo(code_text)
        if promo_code:
            cart.apply_promo_code(promo_code)
            messages.success(request, f'Промокод "{promo_code.code}" успешно применен.')
        else:
            cart.remove_promo_code()
            messages.error(request, 'Этот промокод недействителен или срок его действия истек.')
    return redirect('cart:cart_detail')

@require_POST
def promo_code_remove(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if cart.promo_code:
        messages.info(request, f'Промокод "{cart.promo_code.code}" был удален.')
        cart.remove_promo_code()
    return redirect('cart:cart_detail')