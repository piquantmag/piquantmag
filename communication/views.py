from django.views import generic


class PrivacyPolicyView(generic.TemplateView):
    template_name = 'communication/privacy_policy.html'
