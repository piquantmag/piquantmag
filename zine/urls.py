from django.urls import path, include

from zine import views

urlpatterns = [
    path('<slug:magazine_slug>/', include([
        path('<slug:article_slug', views.article, name='article')
    ]))
]