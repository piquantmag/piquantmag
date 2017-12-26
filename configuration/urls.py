from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('landing.urls', namespace='landing')),
]

if settings.DEBUG:
    urlpatterns += [
        path('404/', TemplateView.as_view(template_name='404.html'), name='page_not_found'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='server_error'),
    ]
