from django.urls import path, include

from zine import views


app_name = 'zine'

urlpatterns = [
    path('<slug:issue_slug>/', include([
        path('', views.IssueView.as_view(), name='issue'),
        path('<slug:article_slug>/', views.ArticleView.as_view(), name='article'),
    ]))
]