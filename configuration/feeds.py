from django.conf import settings
from django.contrib.syndication.views import Feed

from zine.models import Issue


class IssueFeed(Feed):
    title = settings.SITE_NAME
    link = '/feed'
    description = settings.DEFAULT_PAGE_DESCRIPTION
    description_template = 'feeds/issue.html'

    def items(self):
        return Issue.published_issues.all()

    def item_title(self, item):
        return f'{item} | Piquant'
