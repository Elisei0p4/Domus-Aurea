from django import template
from ..models import Article, Tag
from django.db.models import Count

register = template.Library()

@register.simple_tag
def get_most_commented_articles(count=5):
    return Article.objects.filter(is_published=True).annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments', '-views')[:count]

@register.simple_tag
def get_all_tags():
    return Tag.objects.all()