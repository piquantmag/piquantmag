from django.urls import path

import landing.views


app_name = 'landing'


urlpatterns = [
    path('', landing.views.LandingView.as_view(), name='landing'),
]
