from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from zine import models, views


class ArticleViewTestCase(TestCase):
    def test_article_routing_when_not_published(self):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        client = Client()
        article_url = reverse('zine:article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(article_url)
        self.assertEqual(404, response.status_code)

        amp_article_url = reverse('zine:amp_article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(amp_article_url)
        self.assertEqual(404, response.status_code)

    def test_article_routing_when_not_published_with_staff_user(self):
        factory = RequestFactory()
        user = User.objects.create(
            username='test_staff_user',
            email='test@staffuser.com',
            password='s3cr3t',
            is_staff=True
        )
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
            issue=issue,
        )

        article_url = reverse('zine:article', kwargs={'issue_slug': issue.slug, 'article_slug': article.slug})
        request = factory.get(article_url)
        request.user = user
        response = views.ArticleView.as_view()(request, issue_slug=issue.slug, article_slug=article.slug)
        self.assertEqual(200, response.status_code)

        amp_article_url = reverse('zine:amp_article', kwargs={'issue_slug': issue.slug, 'article_slug': article.slug})
        request = factory.get(amp_article_url)
        request.user = user
        response = views.ArticleView.as_view()(request, issue_slug=issue.slug, article_slug=article.slug)
        self.assertEqual(200, response.status_code)

    def test_article_routing_when_published(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
            publication_date=timezone.now(),
        )
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
            issue=issue,
        )

        client = Client()
        article_url = reverse('zine:article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(article_url)
        self.assertEqual(200, response.status_code)

        amp_article_url = reverse('zine:amp_article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(amp_article_url)
        self.assertEqual(200, response.status_code)


class ArticlePreviewViewTestCase(TestCase):
    def test_article_preview_routing_when_not_published(self):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        article_preview = models.ArticlePreview.objects.create(article=article)
        client = Client()
        article_preview_url = reverse('zine:article_preview', kwargs={'uuid': article_preview.uuid})
        response = client.get(article_preview_url)
        self.assertEqual(200, response.status_code)

    def test_article_preview_routing_when_published(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
            publication_date=timezone.now(),
        )

        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
            issue=issue,
        )

        article_preview = models.ArticlePreview.objects.create(article=article)
        client = Client()
        article_preview_url = reverse('zine:article_preview', kwargs={'uuid': article_preview.uuid})
        response = client.get(article_preview_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            reverse('zine:article', kwargs={'issue_slug': issue.slug, 'article_slug': article.slug}),
            response.url,
        )


class IssueViewTestCase(TestCase):
    def test_issue_routing_when_not_published(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )

        client = Client()
        issue_url = reverse('zine:issue', kwargs={'issue_slug': issue.slug})
        response = client.get(issue_url)
        self.assertEqual(404, response.status_code)

    def test_issue_routing_when_published(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
            publication_date=timezone.now(),
        )

        client = Client()
        issue_url = reverse('zine:issue', kwargs={'issue_slug': issue.slug})
        response = client.get(issue_url)
        self.assertEqual(200, response.status_code)

    def test_issue_routing_when_not_published_with_staff_user(self):
        factory = RequestFactory()
        user = User.objects.create(
            username='test_staff_user',
            email='test@staffuser.com',
            password='s3cr3t',
            is_staff=True
        )
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )

        issue_url = reverse('zine:issue', kwargs={'issue_slug': issue.slug})
        request = factory.get(issue_url)
        request.user = user
        response = views.IssueView.as_view()(request, issue_slug=issue.slug)
        self.assertEqual(200, response.status_code)
