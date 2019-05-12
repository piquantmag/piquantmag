from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from zine import models


@pytest.mark.django_db
class TestAuthor:
    def test_author_string_is_display_name(self):
        author = models.Author.objects.create(given_names='Dane', family_names='Hillard', display_name='Dane Hillard')
        assert str(author) == 'Dane Hillard'


@pytest.mark.django_db
class TestPublishedIssueManager:
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
        assert published_issue in published_issues
        assert unpublished_issue not in published_issues


@pytest.mark.django_db
class TestIssue:
    def test_is_published_when_publication_date_in_past(self):
        published_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
        )

        assert published_issue.is_published()

    def test_is_published_when_publication_date_in_future(self):
        unpublished_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now() + timedelta(hours=1),
        )

        assert not unpublished_issue.is_published()

    def test_is_published_when_no_publication_date(self):
        unpublished_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
        )

        assert not unpublished_issue.is_published()

    def test_get_absolute_url(self):
        issue = models.Issue.objects.create(
            title='Some Issue',
            slug='some-issue',
        )

        assert issue.get_absolute_url() == reverse('zine:issue', kwargs={'issue_slug': 'some-issue'})

    def test_string_method(self):
        issue = models.Issue.objects.create(
            title='An Issue Title',
            slug='an-issue-title',
        )

        assert str(issue) == 'An Issue Title'


@pytest.mark.django_db
class TestArticle:
    def test_is_published_when_no_issue(self):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        assert not article.is_published()

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

        assert not article.is_published()

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

        assert article.is_published()

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

        assert article.get_absolute_url() == reverse(
            'zine:article',
            kwargs={'issue_slug': issue.slug, 'article_slug': article.slug},
        )

    def test_str_method(self):
        article = models.Article.objects.create(
            title='Some Article',
            slug='some-article',
        )

        assert str(article) == 'Some Article'
