from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from store.models import Product
from .wishlist import Wishlist

@require_POST
def wishlist_add(request: HttpRequest, product_id: int) -> JsonResponse:
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.add(product)
    return JsonResponse({'status': 'ok', 'count': len(wishlist)})

@require_POST
def wishlist_remove(request: HttpRequest, product_id: int) -> JsonResponse:
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.remove(product)
    return JsonResponse({'status': 'ok', 'count': len(wishlist)})

def wishlist_detail(request: HttpRequest) -> HttpResponse:
    wishlist = Wishlist(request)
    return render(request, 'wishlist/detail.html', {'wishlist': wishlist})