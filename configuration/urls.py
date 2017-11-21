from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^', include('landing.urls', namespace='landing')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404$', TemplateView.as_view(template_name='404.html'), name='page_not_found'),
        url(r'^500$', TemplateView.as_view(template_name='500.html'), name='server_error'),
    ]
