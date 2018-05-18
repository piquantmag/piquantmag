from django.urls import path

import communication.views


app_name = 'communication'


urlpatterns = [
    path('privacy-policy/', communication.views.PrivacyPolicyView.as_view(), name='privacy-policy'),
]
