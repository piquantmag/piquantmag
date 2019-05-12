from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone

from configuration import sitemaps
from zine import models


@pytest.fixture
def get_sitemap_class():
    def _get_sitemap_class(sitemap_type):
        return {
            'issue': sitemaps.IssueSitemap,
            'article': sitemaps.ArticleSitemap,
            'miscellaneous': sitemaps.MiscellaneousPageSitemap,
        }.get(sitemap_type)
    return _get_sitemap_class


@pytest.fixture
def example_pages():
    return [
        'someapp:somepage',
        'someotherapp:somepage',
    ]


@pytest.mark.django_db
class TestIssueSiteMap:
    def test_issue_sitemap_when_no_issues(self, get_sitemap_class):
        sitemap = get_sitemap_class('issue')()
        assert list(sitemap.items()) == []

    def test_issue_sitemap_when_no_published_issues(self, get_sitemap_class):
        sitemap = get_sitemap_class('issue')()

        models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='An unpublished issue',
        )
        assert list(sitemap.items()) == []

    def test_issue_sitemap_when_published_issues(self, get_sitemap_class):
        sitemap = get_sitemap_class('issue')()

        issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
            synopsis='A published issue',
        )
        assert issue in sitemap.items()
        assert sitemap.lastmod(issue) == issue.updated_time


@pytest.mark.django_db
class TestArticleSiteMap:
    def test_article_sitemap_when_no_articles(self, get_sitemap_class):
        sitemap = get_sitemap_class('article')()
        assert list(sitemap.items()) == []

    def test_article_sitemap_when_no_published_articles(self, get_sitemap_class):
        sitemap = get_sitemap_class('article')()

        issue = models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='An unpublished issue',
        )

        models.Article.objects.create(
            title='Unpublished Article',
            slug='unpublished-article',
            issue=issue,
            synopsis='An unpublished issue',
        )

        assert list(sitemap.items()) == []

    def test_article_sitemap_when_published_articles(self, get_sitemap_class):
        sitemap = get_sitemap_class('article')()

        issue = models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now(),
            synopsis='An unpublished issue',
        )

        article = models.Article.objects.create(
            title='Unpublished Article',
            slug='unpublished-article',
            issue=issue,
            synopsis='An unpublished issue',
        )

        assert article in sitemap.items()
        assert sitemap.lastmod(article) == article.updated_time


@pytest.mark.django_db
class TestMiscellaneousPagesSitemap:
    def test_lastmod(self, get_sitemap_class, example_pages):
        sitemap = get_sitemap_class('miscellaneous')(example_pages)

        expected = timezone.now()
        actual = sitemap.lastmod(None)
        assert (actual.year, actual.month, actual.day, actual.hour, actual.minute) == (expected.year, expected.month, expected.day, expected.hour, expected.minute)

    def test_location(self, get_sitemap_class, example_pages):
        sitemap = get_sitemap_class('miscellaneous')(example_pages)

        for name in sitemap.names:
            with mock.patch('configuration.sitemaps.reverse') as mock_reverse:
                sitemap.location(name)
                mock_reverse.assert_called_once_with(name)

    def test_items(self, get_sitemap_class, example_pages):
        sitemap = get_sitemap_class('miscellaneous')(example_pages)
        assert sitemap.items() == example_pages
