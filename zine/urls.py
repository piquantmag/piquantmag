from django.urls import path, include

from zine import views


app_name = 'zine'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('manifest.json', views.ManifestView.as_view(), name='manifest'),
    path('browserconfig.xml', views.BrowserConfigView.as_view(), name='browserconfig'),
    path('preview/<uuid:uuid>/', views.ArticlePreviewView.as_view(), name='article_preview'),
    path('preview/<slug:article_slug>/', views.ArticlePreviewGetOrCreateView.as_view(), name='article_preview_get_or_create'),
    path('amp/<slug:issue_slug>/', include([
        path('<slug:article_slug>/', views.AmpArticleView.as_view(), name='amp_article'),
    ])),
    path('<slug:issue_slug>/', include([
        path('', views.IssueView.as_view(), name='issue'),
        path('<slug:article_slug>/', views.ArticleView.as_view(), name='article'),
    ]))
]
