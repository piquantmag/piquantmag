from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView

import debug_toolbar

import about.urls
import communication.urls
import styleguide.urls
import zine.urls
from configuration import feeds, sitemaps

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_TITLE

full_sitemap = {
    'issues': sitemaps.IssueSitemap,
    'articles': sitemaps.ArticleSitemap,
    'miscellaneous': sitemaps.MiscellaneousPageSitemap([
        'zine:home',
        'communication:newsletter',
    ])
}

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]

urlpatterns += [
    path(settings.ADMIN_URL, admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': full_sitemap}, name='sitemap'),
    path('feed/', feeds.IssueFeed(), name='feed'),
    path('about/', include(about.urls)),
    path('styleguide/', include(styleguide.urls)),
    path('service-worker.js', TemplateView.as_view(template_name='service-worker.js', content_type='application/javascript'), name='service_worker'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('', include(communication.urls)),
    path('', include(zine.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path('404/', TemplateView.as_view(template_name='404.html'), name='page_not_found'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='server_error'),
    ]

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
