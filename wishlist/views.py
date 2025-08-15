from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .wishlist import Wishlist

def wishlist_detail(request: HttpRequest) -> HttpResponse:
    wishlist = Wishlist(request)
    
    return render(request, 'wishlist/detail.html', {
        'wishlist': wishlist,
    })