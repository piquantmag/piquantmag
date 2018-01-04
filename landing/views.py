from django.views import generic


class LandingView(generic.TemplateView):
    template_name = 'landing/landing.html'
