import factory
from factory.django import DjangoModelFactory
from .models import Tag, Article, Comment
from store.factories import UserFactory

class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Тег {n}')
    slug = factory.Sequence(lambda n: f'tag-{n}')

class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Sequence(lambda n: f'Статья {n}')
    slug = factory.Sequence(lambda n: f'article-{n}')
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('paragraph', nb_sentences=10)
    is_published = True

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    article = factory.SubFactory(ArticleFactory)
    author_name = factory.Faker('name')
    email = factory.Faker('email')
    body = factory.Faker('sentence')
    is_active = True
    parent = None