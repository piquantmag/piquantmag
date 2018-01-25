from django.urls import path, include

from zine import views


app_name = 'zine'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('manifest.json', views.ManifestView.as_view(), name='manifest'),
    path('browserconfig.xml', views.BrowserConfigView.as_view(), name='browserconfig'),
    path('<slug:issue_slug>/', include([
        path('', views.IssueView.as_view(), name='issue'),
        path('<slug:article_slug>/', views.ArticleView.as_view(), name='article'),
    ]))
]
