from zine import component_renderers


class ComponentRendererFactory(object):
    def __new__(cls, component):
        return getattr(component_renderers, component.type)(component)
