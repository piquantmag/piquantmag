import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from zine import models, views


@pytest.mark.django_db
class TestArticleView:
    def test_article_routing_when_not_published(self, client):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        article_url = reverse('zine:article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(article_url)
        assert response.status_code == 404

        amp_article_url = reverse('zine:amp_article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(amp_article_url)
        assert response.status_code == 404

    def test_article_routing_when_not_published_with_staff_user(self, rf):
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
        request = rf.get(article_url)
        request.user = user
        response = views.ArticleView.as_view()(request, issue_slug=issue.slug, article_slug=article.slug)
        assert response.status_code == 200

        amp_article_url = reverse('zine:amp_article', kwargs={'issue_slug': issue.slug, 'article_slug': article.slug})
        request = rf.get(amp_article_url)
        request.user = user
        response = views.ArticleView.as_view()(request, issue_slug=issue.slug, article_slug=article.slug)
        assert response.status_code == 200

    def test_article_routing_when_published(self, client):
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

        article_url = reverse('zine:article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(article_url)
        assert response.status_code == 200

        amp_article_url = reverse('zine:amp_article', kwargs={'issue_slug': None, 'article_slug': article.slug})
        response = client.get(amp_article_url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestArticlePreviewView:
    def test_article_preview_routing_when_not_published(self, client):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        article_preview = models.ArticlePreview.objects.create(article=article)
        article_preview_url = reverse('zine:article_preview', kwargs={'uuid': article_preview.uuid})
        response = client.get(article_preview_url)
        assert response.status_code == 200

    def test_article_preview_routing_when_published(self, client):
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
        article_preview_url = reverse('zine:article_preview', kwargs={'uuid': article_preview.uuid})
        response = client.get(article_preview_url)
        assert response.status_code == 302
        assert response.url == reverse('zine:article', kwargs={'issue_slug': issue.slug, 'article_slug': article.slug})


@pytest.mark.django_db
class TestIssueView:
    def test_issue_routing_when_not_published(self, client):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )

        issue_url = reverse('zine:issue', kwargs={'issue_slug': issue.slug})
        response = client.get(issue_url)
        assert response.status_code == 404

    def test_issue_routing_when_published(self, client):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
            publication_date=timezone.now(),
        )

        issue_url = reverse('zine:issue', kwargs={'issue_slug': issue.slug})
        response = client.get(issue_url)
        assert response.status_code == 200

    def test_issue_routing_when_not_published_with_staff_user(self, rf):
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
        request = rf.get(issue_url)
        request.user = user
        response = views.IssueView.as_view()(request, issue_slug=issue.slug)
        assert response.status_code == 200
