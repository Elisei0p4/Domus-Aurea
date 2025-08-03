# store/management/commands/seed_db.py

import random
import os
import shutil
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File
from slugify import slugify
from django.core.cache import cache  # ИМПОРТИРУЕМ КЭШ

from store.models import Category, Product, Review
from blog.models import Tag, Article, Comment
from blog.factories import TagFactory, ArticleFactory, CommentFactory
from store.factories import UserFactory, ReviewFactory

# --- КОНСТАНТЫ ---
NUM_USERS = 15
NUM_TAGS = 15
NUM_ARTICLES = 25
PRODUCTS_PER_CATEGORY_MIN = 16
PRODUCTS_PER_CATEGORY_MAX = 24
REVIEWS_PER_PRODUCT_MAX = 8
COMMENTS_PER_ARTICLE_MAX = 8

# Новые константы для управления скидками
DISCOUNT_CHANCE = 0.3
DISCOUNT_MIN = 15
DISCOUNT_MAX = 75

FURNITURE_TYPES = {
    'Шкафы': ['шкаф 4-х створчатый', 'шкаф-купе', 'шкаф 2-х дверный', 'пенал'],
    'Диваны': ['диван-кровать', 'угловой диван', 'софа'],
    'Кресла': ['кресло', 'кресло-качалка', 'пуф'],
    'Кровати': ['кровать двуспальная', 'кровать с подъемным механизмом', 'тахта'],
    'Столы': ['стол обеденный', 'журнальный столик', 'стол письменный'],
    'Стулья': ['стул кухонный', 'барный стул', 'табурет'],
    'Хранение': ['комод', 'стеллаж', 'тумба под ТВ'],
    'Освещение': ['люстра потолочная', 'торшер', 'настольная лампа'],
}
ADJECTIVES = ['Тивина', 'Орион', 'Вега', 'Норд', 'Лофт', 'Сканди', 'Прованс', 'Модерн', 'Классика']

def get_wardrobe_chars():
    return {
        "Габаритные размеры": { "Ширина, см": f"{random.uniform(120.0, 240.0):.1f}", "Глубина, см": f"{random.uniform(45.0, 65.0):.1f}", "Высота, см": f"{random.uniform(200.0, 240.0):.1f}" },
        "Дополнительные характеристики": { "Цвет фасада": "Белый", "Цвет корпуса": "Дуб сонома", "Материал фасадов": "ЛДСП 16 мм", "Материал задней стенки": "ДВП 3 мм", "Материал корпуса": "ЛДСП 16 мм", "Фасады глянец": random.choice(["Нет", "Да"]), "Количество дверей": random.choice(["Две", "Три", "Четыре"]), "Штанга для белья": "Да", "Нагрузка на штангу": "15 кг", "Тип штанги": random.choice(["Продольная", "Выдвижная"]), "Наличие зеркал": random.choice(["Да", "Нет"]), "Гарантия": "24 месяца" }
    }

def get_sofa_chars():
    return {
        "Габаритные размеры": { "Ширина, см": f"{random.uniform(180.0, 280.0):.1f}", "Глубина, см": f"{random.uniform(80.0, 110.0):.1f}", "Высота, см": f"{random.uniform(70.0, 95.0):.1f}" },
        "Дополнительные характеристики": { "Механизм трансформации": random.choice(["Еврокнижка", "Дельфин", "Аккордеон", "Нет"]), "Материал обивки": "Велюр", "Наполнитель": "ППУ, пружинный блок 'змейка'", "Ящик для белья": "Да", "Максимальная нагрузка": "300 кг", "Гарантия": "18 месяцев" }
    }

CHAR_GENERATORS = { 'Шкафы': get_wardrobe_chars, 'Диваны': get_sofa_chars, 'Кресла': get_sofa_chars, 'Кровати': get_wardrobe_chars, 'Столы': get_wardrobe_chars, 'Стулья': get_wardrobe_chars, 'Хранение': get_wardrobe_chars, 'Освещение': get_sofa_chars }


class Command(BaseCommand):
    help = 'Seeds the database with new, realistic and relevant data, including images.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("= НАЧАЛО ПРОЦЕССА НАПОЛНЕНИЯ БАЗЫ ДАННЫХ ="))
        
        self.stdout.write("--> Шаг 1: Удаление старых данных и изображений...")
        Comment.objects.all().delete(); Article.objects.all().delete(); Tag.objects.all().delete()
        Review.objects.all().delete(); Product.objects.all().delete()
        Category.objects.all().delete(); User.objects.filter(is_superuser=False).delete()
        
        media_path = settings.MEDIA_ROOT
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Не удалось удалить {file_path}. Причина: {e}'))
        os.makedirs(media_path, exist_ok=True)
        
        self.stdout.write(self.style.SUCCESS("    Старые данные успешно удалены."))

        self.stdout.write("--> Шаг 2: Создание новых данных...")
        
        users = UserFactory.create_batch(NUM_USERS)
        users.append(UserFactory(username='testuser', password='password123'))
        tags = TagFactory.create_batch(NUM_TAGS)
        for _ in range(NUM_ARTICLES):
            article = ArticleFactory(author=random.choice(users), tags=random.sample(tags, k=random.randint(1, 4)))
            CommentFactory.create_batch(random.randint(0, COMMENTS_PER_ARTICLE_MAX), article=article, author_name=random.choice(users).get_full_name())
        
        self.stdout.write(f"    - Создание категорий, товаров и отзывов...")
        
        base_seed_image_dir = os.path.join(settings.BASE_DIR, 'seed_data', 'images')

        for category_name, product_types in FURNITURE_TYPES.items():
            category = Category.objects.create(name=category_name, slug=slugify(category_name))
            
            category_image_dir = os.path.join(base_seed_image_dir, category_name)
            image_files = []
            if os.path.exists(category_image_dir):
                image_files = [f for f in os.listdir(category_image_dir) if os.path.isfile(os.path.join(category_image_dir, f))]
            
            random.shuffle(image_files)
            num_images = len(image_files)
            
            if num_images == 0:
                self.stdout.write(self.style.WARNING(f"    ! Для категории '{category_name}' не найдены изображения. Товары будут без картинок."))
            
            num_products_to_create = random.randint(PRODUCTS_PER_CATEGORY_MIN, PRODUCTS_PER_CATEGORY_MAX)
            
            if num_products_to_create > num_images > 0:
                 self.stdout.write(self.style.NOTICE(f"    - Для '{category_name}' будет создано {num_products_to_create} товаров, но доступно лишь {num_images} уникальных изображений. Картинки будут повторяться."))

            char_generator = CHAR_GENERATORS.get(category_name, get_sofa_chars)
            
            for i in range(num_products_to_create):
                product_name = f"{random.choice(product_types)} {random.choice(ADJECTIVES)}"
                product_slug = f"{slugify(product_name)}-{category.slug}-{i}"
                product_brand = random.choice(["Нонтон", "Micasa", "Brayant Group", "Hoff", "Domus Aurea"])
                
                discount = 0
                if random.random() < DISCOUNT_CHANCE:
                    discount = random.randint(DISCOUNT_MIN, DISCOUNT_MAX)
                
                product = Product.objects.create(
                    name=product_name.capitalize(),
                    slug=product_slug,
                    category=category,
                    brand=product_brand,
                    characteristics=char_generator(),
                    base_price=random.randint(15000, 150000),
                    stock=random.randint(5, 50),
                    discount=discount,
                    description="Это прекрасный товар, созданный из лучших материалов с любовью и заботой. Он идеально впишется в ваш интерьер и будет радовать вас долгие годы."
                )

                if num_images > 0:
                    original_image_name = image_files[i % num_images]
                    _, extension = os.path.splitext(original_image_name)
                    new_image_name = f"{product.slug}-{product.id}{extension}"
                    
                    source_image_path = os.path.join(category_image_dir, original_image_name)
                    
                    with open(source_image_path, 'rb') as f:
                        product.image.save(new_image_name, File(f), save=True)

                # Создание отзывов
                num_reviews = random.randint(0, REVIEWS_PER_PRODUCT_MAX)
                if num_reviews > 0:
                    is_good_product = random.random() < 0.75
                    for _ in range(num_reviews):
                        rating = random.choices([3, 4, 5], weights=[1, 4, 5], k=1)[0] if is_good_product else random.choices([1, 2, 3], weights=[4, 3, 1], k=1)[0]
                        ReviewFactory(product=product, author=random.choice(users), rating=rating)

        self.stdout.write(self.style.SUCCESS("--> Шаг 2 завершен: Новые данные успешно созданы."))
        
        # --- ШАГ 3: ОЧИСТКА КЭША ---
        self.stdout.write("--> Шаг 3: Очистка кэша Django...")
        cache.clear()
        self.stdout.write(self.style.SUCCESS("    Кэш успешно очищен."))
        
        self.stdout.write(self.style.SUCCESS("= БАЗА ДАННЫХ УСПЕШНО НАПОЛНЕНА! ="))