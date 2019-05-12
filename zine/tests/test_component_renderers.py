from unittest import mock

import pytest
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from zine import component_renderers


class MockComponentRenderer(component_renderers.ComponentRenderer):
    def html(self):
        return 'some html'

    def admin_string(self):
        return 'some admin string'

    def __str__(self):
        return 'I am a mock component!'


@pytest.fixture
def body_component():
    component = mock.Mock()
    component.body.raw = '# foo'
    component.body.rendered = '<h1>foo</h1>'
    return component


@pytest.fixture
def body_renderer(body_component):
    return component_renderers.BodyComponentRenderer(body_component)


@pytest.fixture
def image_component():
    component = mock.Mock()
    component.image.alt_text = 'very alt'
    component.image.image.url = 'https://foo.com/foo.jpg'
    component.image_alt_text_override = None
    component.image_caption = None
    return component


@pytest.fixture
def image_renderer(image_component):
    return component_renderers.ImageComponentRenderer(image_component)


@pytest.fixture
def pullquote_component():
    component = mock.Mock()
    component.quote = 'foo'
    return component


@pytest.fixture
def pullquote_renderer(pullquote_component):
    return component_renderers.PullQuoteComponentRenderer(pullquote_component)


class TestComponentRenderer:
    def test_base_class_is_abstract(self):
        with pytest.raises(TypeError):
            component_renderers.ComponentRenderer('can\'t do this')

    def test_amphtml_returns_html_by_default(self):
        component = mock.Mock()
        amphtml = MockComponentRenderer(component).amphtml()
        assert amphtml == 'some html'


class TestBodyComponentRenderer:
    def test_html(self, body_renderer):
        assert body_renderer.html == mark_safe('<h1>foo</h1>')

    def test_admin_string(self, body_component, body_renderer):
        assert body_renderer.admin_string == truncatechars(
            body_component.body.raw,
            component_renderers.ADMIN_FIELD_TRUNCATE_LENGTH
        )

    def test_string_method(self, body_component, body_renderer):
        assert str(body_renderer) == body_component.body.raw


class TestImageComponentRenderer:
    def test_alt_text_when_no_override(self, image_renderer):
        assert image_renderer.alt_text == 'very alt'

    def test_alt_text_when_overriden(self, image_component, image_renderer):
        image_component.image_alt_text_override = 'new alt'
        assert image_renderer.alt_text == 'new alt'

    def test_html_without_caption(self, image_component, image_renderer):
        image_component.image_caption = mock.Mock()
        image_component.image_caption.raw = None
        assert image_renderer.html == mark_safe('<img src="https://foo.com/foo.jpg" alt="very alt" />')

    def test_html_with_caption(self, image_component, image_renderer):
        image_component.image_caption = mock.Mock()
        image_component.image_caption.rendered = '<p>foobar</p>'
        assert image_renderer.html == mark_safe(
            '<img src="https://foo.com/foo.jpg" alt="very alt" /><div class="img-caption"><p>foobar</p></div>'
        )

    def test_amphtml_without_caption(self, image_component, image_renderer):
        image_component.image_caption = mock.Mock()
        image_component.image_caption.raw = None
        image_component.image.width = 1
        image_component.image.height = 2
        assert image_renderer.amphtml == mark_safe(
            '<amp-img src="https://foo.com/foo.jpg" width="1" height="2" layout="responsive"></amp-img>'
        )

    def test_amphtml_with_caption(self, image_component, image_renderer):
        image_component.image_caption = mock.Mock()
        image_component.image_caption.rendered = '<p>foobar</p>'
        image_component.image.width = 1
        image_component.image.height = 2
        assert image_renderer.amphtml == mark_safe(
            '<amp-img src="https://foo.com/foo.jpg" width="1" height="2" layout="responsive"></amp-img><div class="img-caption"><p>foobar</p></div>'
        )

    def test_admin_string(self, image_renderer):
        assert image_renderer.admin_string == 'https://foo.com/foo.jpg: very alt'

    def test_string_method(self, image_renderer):
        assert str(image_renderer) == image_renderer.alt_text


class TestPullQuoteComponentRenderer:
    def test_html(self, pullquote_renderer):
        assert pullquote_renderer.html == mark_safe('<blockquote aria-hidden="true">foo</blockquote>')

    def test_admin_string(self, pullquote_component, pullquote_renderer):
        assert pullquote_renderer.admin_string == truncatechars(
            pullquote_component.quote,
            component_renderers.ADMIN_FIELD_TRUNCATE_LENGTH,
        )

    def test_string_method(self, pullquote_component, pullquote_renderer):
        assert str(pullquote_renderer) == pullquote_component.quote
