from django.urls import path

from landing import views


app_name = 'landing'


urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
]
