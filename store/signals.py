from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category, Slide, Feature, SpecialOffer
from blog.models import Article

@receiver([post_save, post_delete], sender=Product)
def clear_product_related_cache(sender, instance, **kwargs):
    """Очищает кэш, связанный с товарами, при их изменении."""
    if instance.category:
        cache.delete(f'similar_products_{instance.category.slug}')
    cache.delete('bestsellers_4')
    print(f"Сигнал от Product '{instance}': Очистка кэша, связанного с товарами.")

@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    """Очищает кэш категорий при их изменении."""
    cache.delete('all_categories')
    cache.delete('home_featured_categories')
    print(f"Сигнал от Category '{instance}': Очистка кэша категорий.")

@receiver([post_save, post_delete], sender=Slide)
def clear_slides_cache(sender, instance, **kwargs):
    """Очищает кэш слайдов на главной."""
    cache.delete('home_slides')
    print(f"Сигнал от Slide '{instance}': Очистка кэша слайдов.")

@receiver([post_save, post_delete], sender=Feature)
def clear_features_cache(sender, instance, **kwargs):
    """Очищает кэш преимуществ на главной."""
    cache.delete('home_features')
    print(f"Сигнал от Feature '{instance}': Очистка кэша преимуществ.")

@receiver([post_save, post_delete], sender=SpecialOffer)
def clear_special_offer_cache(sender, instance, **kwargs):
    """Очищает кэш спецпредложений."""
    cache.delete('active_special_offer')
    print(f"Сигнал от SpecialOffer '{instance}': Очистка кэша спецпредложений.")

@receiver([post_save, post_delete], sender=Article)
def clear_article_cache(sender, instance, **kwargs):
    """Очищает кэш статей на главной при их изменении."""
    cache.delete('home_latest_articles')
    print(f"Сигнал от Article '{instance}': Очистка кэша статей на главной.")