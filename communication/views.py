from django.views import generic


class NewsletterSignupView(generic.TemplateView):
    template_name = 'communication/newsletter.html'
