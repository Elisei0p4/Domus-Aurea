# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from .models import Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from .services import create_order
from django.contrib import messages

@login_required
def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:product_list')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                order = create_order(cart=cart, form_data=request.POST, user=request.user)
                if order:
                    request.session['order_id'] = order.id
                    return redirect(reverse('orders:created'))
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart:cart_detail')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
        
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

def order_created(request: HttpRequest) -> HttpResponse:
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('store:home')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('store:home')
        
    if 'order_id' in request.session:
        del request.session['order_id']

    return render(request, 'orders/created.html', {'order': order})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        total_cost_annotation = Coalesce(
            Sum(F('items__price') * F('items__quantity')),
            0,
            output_field=DecimalField()
        )
        return Order.objects.filter(user=self.request.user) \
                            .annotate(total_cost=total_cost_annotation) \
                            .order_by('-created')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')