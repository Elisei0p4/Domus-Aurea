from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Article, Tag, Comment
from .forms import CommentForm
from django.contrib import messages

def article_list(request, tag_slug=None):
    object_list = Article.objects.filter(is_published=True).select_related('author').prefetch_related('tags')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    context = {
        'page': page,
        'articles': articles,
        'tag': tag
    }
    return render(request, 'blog/list.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    article.views += 1
    article.save(update_fields=['views'])

    comments = article.comments.filter(is_active=True, parent__isnull=True).select_related('parent')
    comment_form = CommentForm()

    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = Article.objects.filter(tags__in=article_tags_ids, is_published=True).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created_at')[:3]

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'similar_articles': similar_articles,
    }
    return render(request, 'blog/detail.html', context)


def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id, is_published=True)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent = get_object_or_404(Comment, id=parent_id)
            
        comment.save()
        messages.success(request, 'Ваш комментарий успешно добавлен и ожидает модерации.')
        return redirect(article.get_absolute_url() + '#comments')
    

    messages.error(request, 'Произошла ошибка при добавлении комментария. Пожалуйста, проверьте форму.')
    
    comments = article.comments.filter(is_active=True, parent__isnull=True)
    similar_articles = Article.objects.filter(tags__in=article.tags.all(), is_published=True).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created_at')[:3]

    context = {
        'article': article,
        'comments': comments,
        'comment_form': form,
        'similar_articles': similar_articles,
    }
    return render(request, 'blog/detail.html', context)