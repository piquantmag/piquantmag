from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.utils.translation import gettext as _

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


class IssueManagerTestCase(TestCase):
    def test_is_published_when_published(self):
        published_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
            synopsis='A published issue',
        )

        self.assertTrue(published_issue.is_published())

    def test_is_published_when_not_published(self):
        unpublished_issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='A published issue',
        )

        self.assertFalse(unpublished_issue.is_published())

    def test_issue_number(self):
        first_issue = models.Issue.objects.create(
            title='First Issue',
            slug='first-issue',
            publication_date=timezone.now(),
            synopsis='The first issue',
        )

        second_issue = models.Issue.objects.create(
            title='Second Issue',
            slug='second-issue',
            publication_date=timezone.now(),
            synopsis='The second issue',
        )

        self.assertEqual(1, first_issue.issue_number)
        self.assertEqual(2, second_issue.issue_number)

    def test_string_method(self):
        issue = models.Issue.objects.create(
            title='An Issue Title',
            slug='an-issue-title',
            publication_date=timezone.now(),
            synopsis='An issue',
        )

        self.assertEqual(_('Issue') + ' 1: An Issue Title', str(issue))