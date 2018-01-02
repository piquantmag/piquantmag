from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from zine.models import Article, Issue


class IssueSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        return Issue.objects.filter(publication_date__lte=timezone.now())

    def lastmod(self, issue):
        return issue.updated_time


class ArticleSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        return Article.objects.filter(issue__publication_date__lte=timezone.now())

    def lastmod(self, article):
        return article.updated_time


class MiscellaneousPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    @staticmethod
    def lastmod(obj):
        return timezone.now()

    def location(self, obj):
        return reverse(obj)
