from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

import about.urls
import communication.urls
import styleguide.urls
import zine.urls
from configuration import feeds, sitemaps


SITE = Site.objects.get_current()

admin.site.site_header = f'{SITE.name} Admin'
admin.site.site_title = SITE.name

full_sitemap = {
    'issues': sitemaps.IssueSitemap,
    'articles': sitemaps.ArticleSitemap,
    'miscellaneous': sitemaps.MiscellaneousPageSitemap([
        'zine:home',
        'communication:newsletter',
    ])
}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': full_sitemap}, name='sitemap'),
    path('feed/', feeds.IssueFeed(), name='feed'),
    path('about/', include(about.urls)),
    path('styleguide/', include(styleguide.urls)),
    path('', include(communication.urls)),
    path('', include(zine.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path('404/', TemplateView.as_view(template_name='404.html'), name='page_not_found'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='server_error'),
    ]
