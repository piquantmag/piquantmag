from django.conf.urls import url

from landing import views


urlpatterns = [
    url(r'^$', views.LandingView.as_view(), name='landing'),
]
