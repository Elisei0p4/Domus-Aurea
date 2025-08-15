import os
import random
import shutil
import subprocess
from django.conf import settings
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from slugify import slugify
from django.core.cache import cache
from django.contrib.auth.models import User

from store.models import Category, Product, ProductImage, Review
from blog.models import Article, Comment, Tag
from store.factories import UserFactory
from blog.factories import ArticleFactory, CommentFactory, TagFactory

# --- БОЛЬШИЕ СПИСКИ ДАННЫХ ДЛЯ МАКСИМАЛЬНОГО РАЗНООБРАЗИЯ ---

# --- 1. Названия товаров ---
STYLES = ['Лофт', 'Сканди', 'Модерн', 'Прованс', 'Классика', 'Хай-тек', 'Минимализм']
COLLECTIONS = ['Орион', 'Вега', 'Тиволи', 'Атлант', 'Сириус', 'Марсель', 'Бруклин', 'Версаль']
MATERIALS = ['из массива дуба', 'из велюра', 'с кожаной обивкой', 'со стеклом', 'из ЛДСП', 'металлический']
COLORS = ['графитовый', 'бежевый', 'изумрудный', 'белый', 'дуб сонома', 'венге', 'кремовый', 'пудровый']

PRODUCT_NAME_TEMPLATES = {
    'Диваны': [
        "Диван трехместный 'Бруклин' велюр", "Угловой диван 'Манхэттен' на ножках", "Диван-кровать 'Осло' в скандинавском стиле",
        "Модульный диван 'Версаль' из экокожи", "Софа 'Прованс' с цветочным принтом", "Диван 'Лофт Индастриал' графитовый",
        "Диван Честерфилд изумрудный", "Прямой диван 'Сканди' бежевый", "Мини-диван 'Токио' для кухни",
    ],
    'Кровати': [
        "Кровать 'Афина' с мягким изголовьем", "Кровать 'Норд' из массива дуба 160x200", "Кровать с подъемным механизмом 'Вега'",
        "Двуспальная кровать 'Ренессанс' с каретной стяжкой", "Кровать-тахта 'Орион' с ящиками", "Кровать 'Хай-тек' с подсветкой",
    ],
    'Шкафы': [
        "Шкаф-купе 'Экспресс' двухдверный", "Шкаф четырехстворчатый 'Классика'", "Пенал 'Слим' для ванной",
        "Распашной шкаф 'Стокгольм' белый", "Угловой шкаф 'Практик' дуб сонома", "Гардеробная система 'Титан'",
    ],
    'Столы': [
        "Обеденный стол 'Галант' раздвижной", "Журнальный столик 'Агат' со стеклом", "Письменный стол 'Минимал' с ящиками",
        "Стол-трансформер 'Акробат'", "Компьютерный стол 'Геймер Про'", "Туалетный столик 'Венеция' с зеркалом",
    ],
    'Стулья': [
        "Стул кухонный 'Комфорт' с мягкой спинкой", "Барный стул 'Космо' на газлифте", "Комплект стульев 'Эко' (4 шт.)",
        "Кресло-стул 'Аристократ' с подлокотниками", "Табурет складной 'Походный'", "Деревянный стул 'Шале'",
    ],
    'Кресла': [
        "Кресло-качалка 'Уют'", "Кресло-мешок 'Груша' XXL", "Реклайнер 'Релакс' с электроприводом",
        "Кресло 'Эгг' в стиле модерн", "Пуф 'Куб' из рогожки", "Кресло 'Папасан' из ротанга",
    ],
    'Хранение': [
        "Комод 'Сорренто' на 4 ящика", "Стеллаж 'Куб' на 8 секций", "Тумба под ТВ 'Медиа'", "Обувница 'Холл' с сиденьем",
        "Витрина 'Кристалл' для посуды", "Настенная полка 'Соты'",
    ],
    'Освещение': [
        "Люстра потолочная 'Каскад' хрустальная", "Торшер 'Арка' с мраморным основанием", "Настольная лампа 'Офис' светодиодная",
        "Подвесной светильник 'Эдисон' в стиле лофт", "Бра 'Ноктюрн' для спальни", "Трековая система 'Спотлайт'",
    ],
}

# --- 2. Описания товаров ---
DESCRIPTIONS = [
    "Эта модель — воплощение современного дизайна и функциональности. Прямые линии, качественные материалы и продуманная эргономика делают её идеальным выбором для любого интерьера. Отлично подойдет для тех, кто ценит комфорт и стиль.",
    "Откройте для себя идеальный баланс между элегантностью и практичностью. Эта модель создана для того, чтобы стать центральным элементом вашей комнаты. Высококачественные материалы гарантируют долгий срок службы и неизменный внешний вид.",
    "Настоящая находка для ценителей уюта. Мягкие формы и приятная на ощупь обивка создают атмосферу тепла и спокойствия. Идеальное место для отдыха после долгого дня. Станет вашим любимым местом в доме.",
    "Практичное и стильное решение для вашего дома. Благодаря компактным размерам, эта модель идеально впишется даже в небольшое пространство, не теряя при этом в функциональности. Вместительные ящики помогут поддерживать порядок.",
    "Роскошь в каждой детали. Эта модель премиум-класса создана для самых взыскательных покупателей. Изысканный дизайн, дорогие материалы и безупречное исполнение подчеркнут ваш статус и утонченный вкус.",
    "Если вы ищете что-то по-настоящему уникальное, обратите внимание на эту модель. Смелый дизайн и необычные цветовые решения сделают ваш интерьер незабываемым. Это не просто мебель, это арт-объект.",
    "Создано для жизни. Прочная конструкция, износостойкие материалы и классический дизайн, который никогда не выйдет из моды. Эта модель будет служить вашей семье верой и правдой на протяжении многих лет.",
    "Идеальное сочетание цены и качества. Эта модель предлагает превосходную функциональность и привлекательный внешний вид по доступной цене. Отличный выбор для тех, кто хочет обновить интерьер без лишних затрат."
]

# --- 3. Характеристики ---
SOFA_MECHANISMS = ["Еврокнижка", "Дельфин", "Аккордеон", "Тик-так", "Французская раскладушка"]
UPHOLSTERY_MATERIALS = ["Велюр", "Рогожка", "Эко-кожа", "Шенилл", "Натуральная кожа", "Флок"]
WARDROBE_COLORS = ["Белый", "Дуб сонома", "Венге", "Графит", "Бетон", "Ясень шимо"]
WARDROBE_MATERIALS = ["ЛДСП 16 мм", "МДФ", "Массив сосны"]

# --- 4. Отзывы (большой пул уникальных отзывов) ---
POSITIVE_REVIEWS = [
    "Превосходное качество! Выглядит даже лучше, чем на фотографиях. Сборка заняла минимум времени, инструкция понятная. Очень довольны покупкой.",
    "Это именно то, что мы искали! Идеально вписался в наш интерьер. Материалы очень приятные на ощупь, сделано все на совесть. Рекомендую!",
    "Доставили точно в срок, хорошо упаковано, ни одной царапины. Мебель превзошла все ожидания. Функционально и очень стильно. Спасибо магазину!",
    "Долго сомневались, но решились и не пожалели. Очень удобный и красивый. Теперь это центральный элемент нашей гостиной. 10 из 10!",
    "Качество на высоте. Фурнитура надежная, все ящики открываются плавно. Чувствуется, что вещь прослужит долго. Определенно стоит своих денег."
]
NEUTRAL_REVIEWS = [
    "В целом, все неплохо. Цвет немного отличается от того, что на сайте, но не критично. Конструкция крепкая, но пришлось повозиться со сборкой.",
    "Нормальный товар за свою цену. Ожидал чуть более качественных материалов, но для своей ценовой категории - вполне достойно. Функции свои выполняет.",
    "Есть пара мелких, почти незаметных сколов на кромке, но решил не возвращать. В остальном все устраивает. Выглядит прилично.",
    "Доставка немного задержалась, но менеджер был на связи. Сам товар соответствует описанию. Посмотрим, как покажет себя в эксплуатации.",
]
NEGATIVE_REVIEWS = [
    "Полное разочарование. Фурнитура самая дешевая, одно из креплений сломалось при сборке. Выглядит гораздо хуже, чем на рекламных фото.",
    "Привезли товар с явным браком - большая царапина на фасаде. Инструкция по сборке ужасная, ничего не понятно. Оформляю возврат.",
    "Не рекомендую. Материалы пахнут химией уже неделю. Конструкция хлипкая, шатается. Зря потраченные деньги и время.",
]

# --- Глобальные константы ---
NUM_USERS = 15; NUM_TAGS = 15; NUM_ARTICLES = 25; REVIEWS_PER_PRODUCT_MAX = 8; COMMENTS_PER_ARTICLE_MAX = 8; IMAGES_PER_PRODUCT_GALLERY = 4
DISCOUNT_CHANCE = 0.3; DISCOUNT_MIN = 15; DISCOUNT_MAX = 75

# --- Улучшенные генераторы характеристик ---
def get_sofa_chars():
    return {
        "Основные параметры": {
            "Ширина, см": f"{random.uniform(180.0, 280.0):.1f}",
            "Глубина, см": f"{random.uniform(80.0, 110.0):.1f}",
            "Высота, см": f"{random.uniform(70.0, 95.0):.1f}"
        },
        "Дополнительные характеристики": {
            "Механизм трансформации": random.choice(SOFA_MECHANISMS),
            "Материал обивки": random.choice(UPHOLSTERY_MATERIALS),
            "Наполнитель": "ППУ, пружинный блок 'змейка'",
            "Ящик для белья": random.choice(["Да", "Нет"]),
            "Максимальная нагрузка, кг": random.choice([250, 300, 350]),
            "Гарантия": "18 месяцев"
        }
    }

def get_wardrobe_chars():
    return {
        "Габаритные размеры": {
            "Ширина, см": f"{random.uniform(120.0, 240.0):.1f}",
            "Глубина, см": f"{random.uniform(45.0, 65.0):.1f}",
            "Высота, см": f"{random.uniform(200.0, 240.0):.1f}"
        },
        "Дополнительные характеристики": {
            "Цвет": random.choice(WARDROBE_COLORS),
            "Материал": random.choice(WARDROBE_MATERIALS),
            "Количество дверей": random.choice([2, 3, 4]),
            "Наличие зеркал": random.choice(["Да", "Нет"]),
            "Тип штанги": random.choice(["Продольная", "Выдвижная"]),
            "Гарантия": "24 месяца"
        }
    }
    
CHAR_GENERATORS = {'Шкафы': get_wardrobe_chars, 'Диваны': get_sofa_chars, 'Кресла': get_sofa_chars, 'Кровати': get_wardrobe_chars, 'Столы': get_wardrobe_chars, 'Стулья': get_wardrobe_chars, 'Хранение': get_wardrobe_chars, 'Освещение': get_sofa_chars}


class Command(BaseCommand):
    help = 'Seeds the database. Prioritizes loading from a dump if available.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("= НАЧАЛО ПРОЦЕССА НАПОЛНЕНИЯ БАЗЫ ДАННЫХ ="))
        
        DUMP_PATH = settings.BASE_DIR / 'seed_data' / 'dump'
        MEDIA_ARCHIVE = DUMP_PATH / 'media_dump.tar.gz'
        
        if os.path.exists(MEDIA_ARCHIVE):
            self.stdout.write(self.style.NOTICE("--> Обнаружен 'снимок' сайта. Загрузка из него..."))
            self.load_from_dump(DUMP_PATH, MEDIA_ARCHIVE)
        else:
            self.stdout.write(self.style.NOTICE("--> 'Снимок' сайта не найден. Запуск процедурной генерации..."))
            self.run_procedural_seeding()
            
        self.stdout.write(self.style.SUCCESS("= БАЗА ДАННЫХ УСПЕШНО НАПОЛНЕНА! ="))

    def load_from_dump(self, dump_path, media_archive):
        self.stdout.write("    - Шаг 1: Очистка базы данных и папки media...")
        call_command('flush', '--no-input')
        
        media_root = settings.MEDIA_ROOT
        if os.path.exists(media_root):
            for filename in os.listdir(media_root):
                file_path = os.path.join(media_root, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Не удалось удалить {file_path}. Причина: {e}'))
        
        self.stdout.write(f"    - Шаг 2: Распаковка архива {media_archive}...")
        shutil.unpack_archive(str(media_archive), str(media_root))
        
        self.stdout.write("    - Шаг 3: Загрузка данных из JSON-фикстур...")
        FIXTURES_ORDER = [
            'user.json', 'category.json', 'product.json', 'productimage.json', 'review.json',
            'feature.json', 'slide.json', 'specialoffer.json', 'tag.json', 'article.json',
            'comment.json', 'promocode.json'
        ]
        
        for fixture_file in FIXTURES_ORDER:
            fixture_path = dump_path / fixture_file
            if os.path.exists(fixture_path):
                self.stdout.write(f"      - Загрузка {fixture_file}...")
                call_command('loaddata', str(fixture_path))
            else:
                 self.stdout.write(self.style.WARNING(f"      - Файл фикстуры {fixture_file} не найден, пропуск."))

        self.stdout.write("    - Шаг 4: Очистка кэша...")
        cache.clear()
        self.stdout.write(self.style.SUCCESS("--> Загрузка из 'снимка' завершена."))

    def run_procedural_seeding(self):
        self.stdout.write("    - Шаг 1: Удаление старых данных и изображений...")
        ProductImage.objects.all().delete(); Review.objects.all().delete(); Product.objects.all().delete()
        Comment.objects.all().delete(); Article.objects.all().delete(); Tag.objects.all().delete()
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
        self.stdout.write(self.style.SUCCESS("      Старые данные успешно удалены."))

        self.stdout.write("    - Шаг 2: Создание новых данных...")
        users = UserFactory.create_batch(NUM_USERS)
        tags = TagFactory.create_batch(NUM_TAGS)
        for _ in range(NUM_ARTICLES):
            article = ArticleFactory(author=random.choice(users), tags=random.sample(tags, k=random.randint(1, 4)))
            CommentFactory.create_batch(random.randint(0, COMMENTS_PER_ARTICLE_MAX), article=article, author_name=random.choice(users).get_full_name())

        base_seed_image_dir = settings.BASE_DIR / 'seed_data' / 'images'
        
        created_products_info = []

        for category_name, product_types in PRODUCT_NAME_TEMPLATES.items():
            category = Category.objects.create(name=category_name, slug=slugify(category_name))
            
            category_image_dir = base_seed_image_dir / category_name
            image_files = [f for f in os.listdir(category_image_dir) if os.path.isfile(category_image_dir / f)] if os.path.exists(category_image_dir) else []
            
            if not image_files:
                self.stdout.write(self.style.WARNING(f"      ! Для категории '{category_name}' не найдены изображения."))
                continue

            num_products = random.randint(len(product_types) // 2, len(product_types))
            
            for i, product_base_name in enumerate(random.sample(product_types, k=num_products)):
                product_name = f"{product_base_name} {random.choice(COLORS)}"
                product_slug = f"{slugify(product_name)}-{category.slug}-{i}"
                sku = f"{category.name[:3].upper()}-{random.randint(10000, 99999)}"

                product = Product(
                    name=product_name.capitalize(), slug=product_slug, category=category,
                    sku=sku, brand=random.choice(COLLECTIONS),
                    characteristics=CHAR_GENERATORS.get(category_name, get_sofa_chars)(),
                    base_price=random.randrange(15000, 150000, 100), stock=random.randint(5, 50),
                    discount=random.randint(DISCOUNT_MIN, DISCOUNT_MAX) if random.random() < DISCOUNT_CHANCE else 0,
                    is_featured=random.random() < 0.2, description=random.choice(DESCRIPTIONS)
                )
                
                main_image_name = random.choice(image_files)
                with open(category_image_dir / main_image_name, 'rb') as f:
                    product.image.save(f"{product.slug}-main.jpg", File(f), save=True)
                
                gallery_images = random.sample(image_files, k=min(len(image_files), IMAGES_PER_PRODUCT_GALLERY))
                for idx, img_name in enumerate(gallery_images):
                    with open(category_image_dir / img_name, 'rb') as f:
                        pi = ProductImage(product=product)
                        pi.image.save(f"{product.slug}-gallery-{idx}.jpg", File(f), save=True)
                
                created_products_info.append({'product': product, 'user_pool': users})

        # Создаем отзывы в отдельном цикле, чтобы гарантировать уникальность
        all_reviews = POSITIVE_REVIEWS + NEUTRAL_REVIEWS + NEGATIVE_REVIEWS
        random.shuffle(all_reviews)

        for info in created_products_info:
            product = info['product']
            num_reviews = random.randint(0, min(REVIEWS_PER_PRODUCT_MAX, len(all_reviews)))
            
            if num_reviews == 0:
                continue

            reviews_for_this_product = random.sample(all_reviews, k=num_reviews)
            all_reviews = [r for r in all_reviews if r not in reviews_for_this_product]

            for review_text in reviews_for_this_product:
                author = random.choice(info['user_pool'])
                
                if review_text in POSITIVE_REVIEWS:
                    rating = random.choice([4, 5])
                elif review_text in NEUTRAL_REVIEWS:
                    rating = 3
                else:
                    rating = random.choice([1, 2])
                
                Review.objects.create(
                    product=product,
                    author=author,
                    author_name=author.get_full_name() or author.username,
                    text=review_text,
                    rating=rating,
                    is_active=True
                )

        self.stdout.write(self.style.SUCCESS("    - Шаг 2 завершен: Новые данные успешно созданы."))
        self.stdout.write("    - Шаг 3: Очистка кэша...")
        cache.clear()
        self.stdout.write(self.style.SUCCESS("      Кэш успешно очищен."))