from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from configuration import feeds
from zine import models


class IssueFeedTestCase(TestCase):
    def setUp(self):
        self.feed = feeds.IssueFeed()

    def test_items_when_no_issues(self):
        self.assertListEqual([], list(self.feed.items()))

    def test_items_when_no_published_issues(self):
        models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='An unpublished issue',
        )

        self.assertListEqual([], list(self.feed.items()))

    def test_items_when_published_issues(self):
        issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
            synopsis='A published issue',
        )

        self.assertIn(issue, self.feed.items())

    def test_item_title(self):
        self.assertEqual('Foo | Piquant', self.feed.item_title('Foo'))
