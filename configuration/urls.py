from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

import about.urls
import configuration.feeds
import configuration.sitemaps
import landing.urls
import zine.urls
import styleguide.urls


SITE = Site.objects.get_current()

admin.site.site_header = f'{SITE.name} Admin'
admin.site.site_title = SITE.name

full_sitemap = {
    'issues': configuration.sitemaps.IssueSitemap,
    'articles': configuration.sitemaps.ArticleSitemap,
    'miscellaneous': configuration.sitemaps.MiscellaneousPageSitemap([
        'landing:landing',
    ])
}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': full_sitemap}, name='sitemap'),
    path('feed/', configuration.feeds.IssueFeed(), name='feed'),
    path('about/', include(about.urls)),
    path('styleguide/', include(styleguide.urls)),
    path('', include(landing.urls)),
    path('', include(zine.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path('404/', TemplateView.as_view(template_name='404.html'), name='page_not_found'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='server_error'),
    ]
