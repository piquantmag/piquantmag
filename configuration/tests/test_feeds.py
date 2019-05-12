from datetime import timedelta

import pytest
from django.utils import timezone

from configuration import feeds
from zine import models


@pytest.fixture
def feed():
    return feeds.IssueFeed()


@pytest.mark.django_db
class TestIssueFeed:
    def test_items_when_no_issues(self, feed):
        assert list(feed.items()) == []

    def test_items_when_no_published_issues(self, feed):
        models.Issue.objects.create(
            title='Unpublished Issue',
            slug='unpublished-issue',
            publication_date=timezone.now() + timedelta(hours=1),
            synopsis='An unpublished issue',
        )

        assert list(feed.items()) == []

    def test_items_when_published_issues(self, feed):
        issue = models.Issue.objects.create(
            title='Published Issue',
            slug='published-issue',
            publication_date=timezone.now(),
            synopsis='A published issue',
        )

        assert issue in feed.items()

    def test_item_title(self, feed):
        assert feed.item_title('Foo') == 'Foo | Piquant'
