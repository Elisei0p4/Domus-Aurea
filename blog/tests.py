from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Tag, Comment
from .templatetags.blog_tags import get_most_commented_articles, get_all_tags
from .factories import ArticleFactory, TagFactory, CommentFactory, UserFactory

class BlogModelAndLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.tag = TagFactory(name='Тег', slug='tag')
        self.article = ArticleFactory(
            title='Тестовая статья', 
            slug='test-article', 
            author=self.user,
            tags=[self.tag]
        )
        self.comment = CommentFactory(article=self.article, author_name='Комментатор')

    def test_article_list_view(self):
        response = self.client.get(reverse('blog:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertTemplateUsed(response, 'blog/list.html')

    def test_article_detail_view(self):
        initial_views = self.article.views
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.comment.body)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.article.refresh_from_db()
        self.assertEqual(self.article.views, initial_views + 1)

    def test_article_list_by_tag_view(self):
        ArticleFactory() 
        response = self.client.get(self.tag.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertIn('tag', response.context)
        self.assertEqual(response.context['tag'], self.tag)
        self.assertEqual(len(response.context['articles']), 1)

    def test_post_comment(self):
        comment_data = {'author_name': 'Новый', 'email': 'new@test.com', 'body': 'Новый коммент.'}
        response = self.client.post(reverse('blog:post_comment', args=[self.article.id]), data=comment_data, follow=True)
        self.assertRedirects(response, self.article.get_absolute_url() + '#comments')
        self.assertTrue(Comment.objects.filter(body=comment_data['body']).exists())
        self.assertEqual(self.article.comments.count(), 2)
        self.assertContains(response, 'Ваш комментарий успешно добавлен')

    def test_post_reply_to_comment(self):
        """Тестирует отправку ответа на комментарий."""
        reply_data = {'author_name': 'Отвечающий', 'email': 'reply@test.com', 'body': 'Это ответ.', 'parent_id': self.comment.id}
        response = self.client.post(reverse('blog:post_comment', args=[self.article.id]), data=reply_data, follow=True)
        self.assertRedirects(response, self.article.get_absolute_url() + '#comments')
        
        reply_comment = Comment.objects.get(body=reply_data['body'])
        self.assertEqual(reply_comment.parent, self.comment)
        self.assertEqual(self.comment.replies.count(), 1)


class BlogTemplateTagTests(TestCase):
    def setUp(self):
        self.a1 = ArticleFactory()
        self.a2 = ArticleFactory()
        CommentFactory(article=self.a1)
        CommentFactory(article=self.a1)
        CommentFactory(article=self.a2)
        
        self.t1 = TagFactory()
        self.t2 = TagFactory()

    def test_get_most_commented_articles(self):
        """Тестирует тег для получения самых комментируемых статей."""
        most_commented = get_most_commented_articles(count=1)
        self.assertEqual(most_commented.count(), 1)
        self.assertEqual(most_commented.first(), self.a1)

    def test_get_all_tags(self):
        """Тестирует тег для получения всех тегов."""
        tags = get_all_tags()
        self.assertEqual(tags.count(), 2)