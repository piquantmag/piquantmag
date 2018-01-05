from django.urls import path

from styleguide import views


app_name = 'styleguide'


urlpatterns = [
    path('', views.StyleguideView.as_view(), name='styleguide'),
]