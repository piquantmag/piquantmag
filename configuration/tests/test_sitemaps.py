from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from configuration import sitemaps
from zine import models


class IssueSiteMapTestCase(TestCase):
    def setUp(self):
        self.sitemap = sitemaps.IssueSitemap()

    def test_issue_sitemap_when_no_issues(self):
        self.assertListEqual([], list(self.sitemap.items()))

    def test_issue_sitemap_when_no_published_issues(self):
        models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='An unpublished issue',
        )
        self.assertListEqual([], list(self.sitemap.items()))

    def test_issue_sitemap_when_published_issues(self):
        issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
            synopsis='A published issue',
        )
        self.assertIn(issue, self.sitemap.items())
        self.assertEqual(issue.updated_time, self.sitemap.lastmod(issue))


class ArticleSiteMapTestCase(TestCase):
    def setUp(self):
        self.sitemap = sitemaps.ArticleSitemap()

    def test_article_sitemap_when_no_articles(self):
        self.assertListEqual([], list(self.sitemap.items()))

    def test_article_sitemap_when_no_published_articles(self):
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

        self.assertListEqual([], list(self.sitemap.items()))

    def test_article_sitemap_when_published_articles(self):
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

        self.assertIn(article, self.sitemap.items())
        self.assertEqual(article.updated_time, self.sitemap.lastmod(article))


class MiscellaneousPagesSitemapTestCase(TestCase):
    def setUp(self):

        self.pages = [
            'someapp:somepage',
            'someotherapp:somepage',
        ]
        self.sitemap = sitemaps.MiscellaneousPageSitemap(self.pages)

    def test_lastmod(self):
        expected = timezone.now()
        actual = self.sitemap.lastmod(None)
        self.assertEqual(expected.year, actual.year)
        self.assertEqual(expected.month, actual.month)
        self.assertEqual(expected.day, actual.day)
        self.assertEqual(expected.hour, actual.hour)
        self.assertEqual(expected.minute, actual.minute)

    def test_location(self):
        for name in self.sitemap.names:
            with mock.patch('configuration.sitemaps.reverse') as mock_reverse:
                self.sitemap.location(name)
                mock_reverse.assert_called_once_with(name)

    def test_items(self):
        self.assertListEqual(self.pages, self.sitemap.items())
