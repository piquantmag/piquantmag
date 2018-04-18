from django.urls import path, include
from rest_framework import routers

from zine import views

app_name = 'zine'


router = routers.SimpleRouter()
router.register('articles', views.ArticleViewSet)
router.register('issues', views.IssueViewSet)
router.register('images', views.ImageViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.HomeView.as_view(), name='home'),

    path('manifest.json', views.ManifestView.as_view(), name='manifest'),
    path('browserconfig.xml', views.BrowserConfigView.as_view(), name='browserconfig'),

    path('preview/<uuid:uuid>/', views.ArticlePreviewView.as_view(), name='article_preview'),
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:article_id>/edit/', views.ArticleEditView.as_view(), name='article_edit'),

    path('amp/<slug:issue_slug>/', include([
        path('<slug:article_slug>/', views.AmpArticleView.as_view(), name='amp_article'),
    ])),

    path('<slug:issue_slug>/', include([
        path('', views.IssueView.as_view(), name='issue'),
        path('<slug:article_slug>/', views.ArticleView.as_view(), name='article'),
    ]))
]
