from django.test import TestCase, Client
from django.urls import reverse

from styleguide import views


class StyleguideViewTestCase(TestCase):
    def test_get_context_data(self):
        context_data = views.StyleguideView().get_context_data()
        self.assertIn('sections', context_data)

        sections = context_data['sections']

        client = Client()
        response = client.get(reverse('styleguide:styleguide'))

        for section in sections:
            self.assertTemplateUsed(response, f'styleguide/components/__i_{section}.html')
