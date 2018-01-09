from django.urls import path

import communication.views


app_name = 'communication'


urlpatterns = [
    path('newsletter/', communication.views.NewsletterSignupView.as_view(), name='newsletter'),
]
