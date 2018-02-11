from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from zine import models


class AuthorTestCase(TestCase):
    def test_author_string_is_display_name(self):
        author = models.Author.objects.create(given_names='Dane', family_names='Hillard', display_name='Dane Hillard')
        self.assertEqual('Dane Hillard', str(author))


class PublishedIssueManagerTest(TestCase):
    def test_manager_returns_only_published_issues(self):
        published_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
            synopsis='A published issue',
        )

        unpublished_issue = models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='An unpublished issue',
        )

        published_issues = models.Issue.published_issues.all()
        self.assertIn(published_issue, published_issues)
        self.assertNotIn(unpublished_issue, published_issues)


class IssueTestCase(TestCase):
    def test_is_published_when_publication_date_in_past(self):
        published_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
        )

        self.assertTrue(published_issue.is_published())

    def test_is_published_when_publication_date_in_future(self):
        unpublished_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now() + timedelta(hours=1),
        )

        self.assertFalse(unpublished_issue.is_published())

    def test_is_published_when_no_publication_date(self):
        unpublished_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
        )

        self.assertFalse(unpublished_issue.is_published())

    def test_get_absolute_url(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )

        self.assertEqual(
            reverse('zine:issue', kwargs={'issue_slug': 'some-issue'}),
            issue.get_absolute_url(),
        )

    def test_string_method(self):
        issue = models.Issue.objects.create(
            title='An Issue Title',
            slug='an-issue-title',
        )

        self.assertEqual('An Issue Title', str(issue))


class ArticleTestCase(TestCase):
    def test_is_published_when_no_issue(self):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        self.assertFalse(article.is_published())

    def test_is_published_when_issue_not_published(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )

        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
            issue=issue,
        )

        self.assertFalse(article.is_published())

    def test_is_published_when_issue_published(self):
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

        self.assertTrue(article.is_published())

    def test_get_absolute_url(self):
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

        self.assertEqual(
            reverse('zine:article', kwargs={'issue_slug': issue.slug, 'article_slug': article.slug}),
            article.get_absolute_url(),
        )

    def test_str_method(self):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        self.assertEqual('Some Article', str(article))
