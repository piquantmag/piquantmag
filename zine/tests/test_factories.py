from unittest import mock

import pytest

from zine import component_renderers
from zine.factories import ComponentRendererFactory


class TestComponentRendererFactory:
    def test_new_return_type_when_component_renderer_exists(self):
        class MockRenderer:
            def __init__(self, *args, **kwargs):
                pass

        component_renderers.MockRenderer = MockRenderer
        component = mock.Mock()
        component.type = 'MockRenderer'
        assert isinstance(ComponentRendererFactory(component), MockRenderer)

    def test_new_return_type_when_component_renderer_does_not_exist(self):
        with pytest.raises(AttributeError):
            component = mock.Mock()
            component.type = 'Not a real renderer!'
            ComponentRendererFactory(component)
