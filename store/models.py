from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(available=True, stock__gt=0)

    def on_sale(self):
        return self.available().filter(discount__gt=0)
    
    def new_arrivals(self, days=30):
        return self.available().filter(created__gte=timezone.now() - timezone.timedelta(days=days))

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def on_sale(self):
        return self.get_queryset().on_sale()

    def new_arrivals(self, days=30):
        return self.get_queryset().new_arrivals(days)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL (слаг)")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение (для главной)")
    is_featured = models.BooleanField(default=False, verbose_name="Показать на главной в новом блоке")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', kwargs={'category_slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Основное изображение")
    
    # Поля для генерации адаптивных изображений для карточек
    image_card_large = ImageSpecField(source='image',
                                      processors=[ResizeToFit(800, 800)],
                                      format='WEBP',
                                      options={'quality': 80})
    image_card_small = ImageSpecField(source='image',
                                      processors=[ResizeToFit(400, 400)],
                                      format='WEBP',
                                      options={'quality': 75})

    brand = models.CharField(max_length=100, blank=True, verbose_name="Бренд")
    collection = models.CharField(max_length=100, blank=True, verbose_name="Коллекция")
    characteristics = models.JSONField(blank=True, null=True, verbose_name="Характеристики")

    model_3d = models.FileField(
        upload_to='products_3d/', 
        blank=True, 
        null=True, 
        verbose_name="3D Модель (.glb)",
        help_text="Загрузите 3D модель товара в формате .glb"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Артикул (SKU)")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена")
    discount = models.PositiveSmallIntegerField(
        default=0, 
        verbose_name="Скидка в %",
        help_text="Укажите скидку в процентах от 0 до 99.",
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена", editable=False)
    stock = models.PositiveIntegerField(verbose_name="Остаток на складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый (на главной)")
    
    purchase_count = models.PositiveIntegerField(default=0, verbose_name="Количество покупок")

    objects = ProductManager()
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [ models.Index(fields=['id', 'slug']), models.Index(fields=['name']), models.Index(fields=['-created']), ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.final_price = self.base_price * (1 - Decimal(self.discount) / 100)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'product_slug': self.slug})
        
    def get_main_image_url(self):
        if self.image:
            return self.image.url
        # Если основного изображения нет, берем первое из галереи
        first_gallery_image = self.images.first()
        if first_gallery_image:
            return first_gallery_image.image.url
        # Если вообще нет изображений
        from django.templatetags.static import static
        return static('images/placeholder.png')

    @property
    def old_price(self):
        if self.discount > 0:
            return self.base_price
        return None

    @property
    def average_rating(self):
        avg = self.reviews.filter(is_active=True).aggregate(Avg('rating'))['rating__avg']
        return avg if avg is not None else 0

    @property
    def review_count(self):
        return self.reviews.filter(is_active=True).count()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Товар")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Изображение")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст")
    
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 80})

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Галерея изображений товара"
        ordering = ['id']

    def __str__(self):
        return f"Изображение для {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Автор", null=True, blank=True)
    author_name = models.CharField(max_length=100, verbose_name="Имя автора (если не зарегистрирован)")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг", choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен (отображается на сайте)")

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    def __str__(self): return f'Отзыв от {self.author_name} на {self.product.name}'

class Feature(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='features/', verbose_name="Иконка/Изображение")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    class Meta:
        ordering = ['display_order']
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
    def __str__(self): return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    def __str__(self): return self.email
    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    class Meta:
        verbose_name = "Сообщение из формы контактов"
        verbose_name_plural = "Сообщения из формы контактов"
        ordering = ['-created_at']
    def __str__(self): return f"Сообщение от {self.name} ({self.email}) на тему '{self.subject}'"

class Slide(models.Model):
    alt_text = models.CharField(max_length=200, verbose_name="Название/Альтернативный текст (для SEO и админки)", default='')
    image = models.ImageField(upload_to='slides/', verbose_name="Изображение для слайда")
    link_url = models.CharField(max_length=255, default='/', verbose_name="URL-адрес для ссылки", help_text="Куда будет вести клик по слайду. Например, /shop/ или /sale/")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    class Meta:
        ordering = ['display_order']
        verbose_name = "Слайд на главной"
        verbose_name_plural = "Слайды на главной"
    def __str__(self): return self.alt_text

class SpecialOfferManager(models.Manager):
    def get_active(self):
        now = timezone.now()
        return self.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-id').first()

class SpecialOffer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название акции (для админки)")
    image = models.ImageField(upload_to='special_offers/', verbose_name="Изображение баннера")
    link_url = models.CharField(max_length=255, blank=True, verbose_name="URL-адрес для ссылки", help_text="Куда будет вести клик по баннеру. Оставьте пустым, если баннер некликабельный.")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст (для SEO)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Дата начала показа")
    end_date = models.DateTimeField(verbose_name="Дата окончания показа")

    objects = SpecialOfferManager()

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Специальное предложение (баннер)"
        verbose_name_plural = "Специальные предложения (баннеры)"

    def __str__(self):
        return self.name