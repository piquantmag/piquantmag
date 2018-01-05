from django.views.generic import TemplateView


class StyleguideView(TemplateView):
    template_name = 'styleguide/styleguide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sections'] = [
            'typography',
            'buttons',
            'forms',
            'links',
            'lists',
            'cards',
        ]

        return context
