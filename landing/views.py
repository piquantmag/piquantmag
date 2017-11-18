from django.shortcuts import render
from django.views import generic


class LandingView(generic.TemplateView):
    template_name = 'landing/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_description'] = 'Sign up for the Piquant newsletter to get status updates about our first issue!'
        return context
