from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed

from zine.models import Issue


SITE = Site.objects.get_current()


class IssueFeed(Feed):
    title = SITE.name
    link = f'//{SITE.domain}'
    description = settings.DEFAULT_PAGE_DESCRIPTION
    description_template = 'feeds/issue.html'

    def items(self):
        return Issue.published_issues.all()

    def item_title(self, item):
        return f'{item} | Piquant'
