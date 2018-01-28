from unittest import mock

from django.test import TestCase

from zine import component_renderers
from zine.factories import ComponentRendererFactory


class ComponentRendererFactoryTestCase(TestCase):
    def test_new_return_type_when_component_renderer_exists(self):
        class MockRenderer:
            def __init__(self, *args, **kwargs):
                pass

        component_renderers.MockRenderer = MockRenderer
        component = mock.Mock()
        component.type = 'MockRenderer'
        self.assertIsInstance(ComponentRendererFactory(component), MockRenderer)

    def test_new_return_type_when_component_renderer_does_not_exist(self):
        with self.assertRaises(AttributeError):
            component = mock.Mock()
            component.type = 'Not a real renderer!'
            ComponentRendererFactory(component)
