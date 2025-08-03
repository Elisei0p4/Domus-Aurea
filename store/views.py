# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum, F, DecimalField
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.templatetags.static import static

from .models import Product, Category, Review, Subscriber, ContactMessage, Feature, Slide
from .forms import ReviewForm, ContactForm
from .filters import ProductFilter
from .services import add_review
from blog.models import Article
from cart.forms import CartAddProductForm
from cart.cart import Cart

def home_view(request):
    slides = cache.get('home_slides')
    if slides is None:
        slides = Slide.objects.filter(is_active=True).order_by('display_order')
        cache.set('home_slides', slides, 60 * 60)

    featured_categories = cache.get('home_featured_categories')
    if featured_categories is None:
        featured_categories = Category.objects.filter(is_featured=True)
        cache.set('home_featured_categories', featured_categories, 60 * 60)

    features = cache.get('home_features')
    if features is None:
        features = Feature.objects.all()
        cache.set('home_features', features, 60 * 60)

    latest_articles = cache.get('home_latest_articles')
    if latest_articles is None:
        try:
            latest_articles = Article.objects.filter(is_published=True)[:3]
        except Exception:
            latest_articles = []
        cache.set('home_latest_articles', latest_articles, 60 * 60)

    context = {
        'slides': slides,
        'latest_articles': latest_articles,
        'featured_categories': featured_categories,
        'features': features,
    }
    return render(request, 'store/home.html', context)


@cache_page(60 * 15)
def product_list_view(request, category_slug=None):
    category = None
    products_list = Product.objects.available()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)

    query = request.GET.get('q')
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    product_filter = ProductFilter(request.GET, queryset=products_list)
    
    filtered_products = product_filter.qs

    if not request.GET.get('ordering'):
         filtered_products = filtered_products.order_by('-created')

    paginator = Paginator(filtered_products, 15) 
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'products': products,
        'filter_form': product_filter.form,
        'query': query,
    }
    return render(request, 'store/shop.html', context)


def product_detail_view(request, product_slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('reviews__author'), 
        slug=product_slug,
        available=True
    )
    
    reviews = product.reviews.filter(is_active=True)
    
    cart_product_form = CartAddProductForm()
    
    review_form = ReviewForm()
    user_has_reviewed = False
    if request.user.is_authenticated:
        if reviews.filter(author=request.user).exists():
            user_has_reviewed = True

    if request.method == 'POST' and 'submit_review' in request.POST:
        if not user_has_reviewed and request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.product = product
                new_review.author = request.user
                new_review.author_name = request.user.get_full_name() or request.user.username
                new_review.save()
                messages.success(request, 'Спасибо за ваш отзыв!')
                return redirect(product.get_absolute_url())
            else:
                review_form = form

    context = {
        'product': product,
        'reviews': reviews,
        'cart_product_form': cart_product_form,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'store/product_detail.html', context)

def buy_now_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    
    if product.stock < 1:
        messages.error(request, 'К сожалению, этот товар закончился.')
        return redirect(product.get_absolute_url())
        
    cart.add(product=product, quantity=1, update_quantity=True)
    return redirect('orders:order_create')


def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            _, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Вы успешно подписались на рассылку!')
            else:
                messages.info(request, 'Этот email уже подписан на рассылку.')
    return redirect(request.META.get('HTTP_REFERER', 'store:home'))


@login_required
def account_view(request):
    total_cost_annotation = Coalesce(
        Sum(F('items__price') * F('items__quantity')),
        0,
        output_field=DecimalField()
    )
    orders = request.user.orders.annotate(total_cost=total_cost_annotation) \
                                .order_by('-created')[:5]
    context = {
        'orders': orders
    }
    return render(request, 'store/account.html', context)


def new_arrivals_view(request):
    products = Product.objects.new_arrivals(days=30)
    context = {
        'products': products,
        'page_title': 'Новинки'
    }
    return render(request, 'store/new_arrivals.html', context)


def sale_view(request):
    products = Product.objects.on_sale()
    context = {
        'products': products,
        'page_title': 'Распродажа'
    }
    return render(request, 'store/sale.html', context)


def about_view(request):
    return render(request, 'store/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                send_mail(
                    subject=f"Новое сообщение с сайта: {contact_message.subject}",
                    message=f"От: {contact_message.name} <{contact_message.email}>\n\n{contact_message.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                )
                messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            except Exception as e:
                messages.error(request, 'Произошла ошибка при отправке сообщения.')
            return redirect('store:contacts')
    else:
        form = ContactForm()
    
    return render(request, 'store/contact.html', {'form': form})


class StaticPageView(TemplateView):
    def get_template_names(self):
        page_name = self.kwargs['page_name']
        return [f"store/static/{page_name}.html"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_titles = {
            'faq': 'Часто задаваемые вопросы (FAQ)', 'privacy': 'Политика конфиденциальности',
            'terms': 'Условия использования', 'delivery': 'Доставка и оплата',
            'returns': 'Возвраты и обмен', 'warranty': 'Гарантия',
            'track-order': 'Отследить заказ',
        }
        context['page_title'] = page_titles.get(kwargs['page_name'], 'Информация')
        return context