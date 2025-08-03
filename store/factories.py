import random
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from .models import Category, Product, Review

class UserFactory(DjangoModelFactory):
    class Meta: 
        model = User
        django_get_or_create = ('username',)
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'a-strong-password')

class CategoryFactory(DjangoModelFactory):
    class Meta: 
        model = Category
        django_get_or_create = ('name',) 
    name = factory.Sequence(lambda n: f'Категория {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')

class ProductFactory(DjangoModelFactory):
    class Meta: 
        model = Product
    name = factory.Faker('word')
    slug = factory.Sequence(lambda n: f'product-{n}')
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    brand = factory.Faker('company')
    collection = factory.Faker('word')
    sku = factory.Sequence(lambda n: f'SKU-{n:05d}')
    base_price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, min_value=1000)
    stock = factory.Faker('random_int', min=1, max=100)
    available = True
    discount = factory.LazyFunction(lambda: random.choices([0, 10, 20, 30, 50], weights=[70, 10, 10, 5, 5])[0])

POSITIVE_TEXTS = [
    "Отличное качество, полностью соответствует описанию. Очень доволен покупкой! Сборка простая, все детали на месте. Выглядит стильно и дорого.",
    "Прекрасный товар, выглядит даже лучше, чем на фото. Материалы качественные, приятные на ощупь. Доставили быстро и в целости. Однозначно рекомендую.",
    "Все супер! Давно искал что-то подобное. Идеально вписался в интерьер. Пользуюсь с удовольствием, никаких нареканий.",
    "Покупка превзошла все ожидания. Функционально, красиво и удобно. Спасибо магазину за отличный сервис и качественный товар.",
]
NEUTRAL_TEXTS = [
    "В целом, неплохо. Есть пара мелких царапин, но не критично, за такую цену можно простить. Своих денег стоит.",
    "Нормальный товар. Ожидал немного большего от материалов, но в целом все устраивает. Функции свои выполняет, сборка заняла около часа.",
    "Цвет немного отличается от того, что на сайте, более тусклый. В остальном все в порядке, конструкция крепкая.",
]
NEGATIVE_TEXTS = [
    "Ужасное качество. Сломалось в первый же день. Крепления хлипкие, материал дешевый. Не рекомендую никому.",
    "Привезли товар с явным браком. Инструкция совершенно непонятная, потратил кучу времени и нервов на сборку. Полное разочарование.",
    "Выглядит очень дешево, совсем не как на картинке. Конструкция шатается. Буду оформлять возврат. Зря потраченные деньги.",
]

def generate_review_text(rating):
    if rating >= 4: return random.choice(POSITIVE_TEXTS)
    if rating == 3: return random.choice(NEUTRAL_TEXTS)
    return random.choice(NEGATIVE_TEXTS)

class ReviewFactory(DjangoModelFactory):
    class Meta: 
        model = Review
    product = factory.SubFactory(ProductFactory)
    author = factory.SubFactory(UserFactory)
    author_name = factory.LazyAttribute(lambda o: o.author.get_full_name() or o.author.username)
    rating = factory.Faker('random_int', min=1, max=5)
    text = factory.LazyAttribute(lambda o: generate_review_text(o.rating))
    is_active = True