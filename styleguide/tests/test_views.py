from django.urls import reverse

from styleguide import views


class TestStyleguideView:
    def test_get_context_data(self, client):
        context_data = views.StyleguideView().get_context_data()
        assert 'sections' in context_data

        sections = context_data['sections']

        response = client.get(reverse('styleguide:styleguide'))

        templates_used = [t.name for t in response.templates]

        for section in sections:
            assert f'styleguide/components/__i_{section}.html' in templates_used
