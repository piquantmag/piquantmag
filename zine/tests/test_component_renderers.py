from unittest import mock

from django.template.defaultfilters import truncatechars
from django.test import TestCase
from django.utils.safestring import mark_safe

from zine import component_renderers


class MockComponentRenderer(component_renderers.ComponentRenderer):
    def html(self):
        return 'some html'

    def admin_string(self):
        return 'some admin string'

    def __str__(self):
        return 'I am a mock component!'


class ComponentRendererTestCase(TestCase):
    def test_base_class_is_abstract(self):
        with self.assertRaises(TypeError):
            component_renderers.ComponentRenderer('can\'t do this')

    def test_amphtml_returns_html_by_default(self):
        component = mock.Mock()
        amphtml = MockComponentRenderer(component).amphtml()
        self.assertEqual('some html', amphtml)


class BodyComponentRendererTestCase(TestCase):
    def setUp(self):
        self.component = mock.Mock()
        self.component.body.raw = '# foo'
        self.component.body.rendered = '<h1>foo</h1>'
        self.renderer = component_renderers.BodyComponentRenderer(self.component)

    def test_html(self):
        self.assertEqual(mark_safe('<h1>foo</h1>'), self.renderer.html)

    def test_admin_string(self):
        self.assertEqual(
            truncatechars(self.component.body.raw, component_renderers.ADMIN_FIELD_TRUNCATE_LENGTH),
            self.renderer.admin_string,
        )

    def test_string_method(self):
        self.assertEqual(
            self.component.body.raw,
            str(self.renderer),
        )


class ImageComponentRendererTestCase(TestCase):
    def setUp(self):
        self.component = mock.Mock()
        self.component.image.alt_text = 'very alt'
        self.component.image.image.url = 'https://foo.com/foo.jpg'
        self.component.image_alt_text_override = None
        self.component.image_caption = None
        self.renderer = component_renderers.ImageComponentRenderer(self.component)

    def test_alt_text_when_no_override(self):
        self.assertEqual('very alt', self.renderer.alt_text)

    def test_alt_text_when_overriden(self):
        self.component.image_alt_text_override = 'new alt'
        self.assertEqual('new alt', self.renderer.alt_text)

    def test_html_without_caption(self):
        self.component.image_caption = mock.Mock()
        self.component.image_caption.raw = None
        self.assertEqual(
            mark_safe('<img src="https://foo.com/foo.jpg" alt="very alt" />'),
            self.renderer.html,
        )

    def test_html_with_caption(self):
        self.component.image_caption = mock.Mock()
        self.component.image_caption.rendered = '<p>foobar</p>'
        self.assertEqual(
            mark_safe(
                '<img src="https://foo.com/foo.jpg" alt="very alt" /><div class="img-caption"><p>foobar</p></div>'
            ),
            self.renderer.html,
        )

    def test_amphtml_without_caption(self):
        self.component.image_caption = mock.Mock()
        self.component.image_caption.raw = None
        self.component.image.width = 1
        self.component.image.height = 2
        self.assertEqual(
            mark_safe('<amp-img src="https://foo.com/foo.jpg" width="1" height="2" layout="responsive"></amp-img>'),
            self.renderer.amphtml,
        )

    def test_amphtml_with_caption(self):
        self.component.image_caption = mock.Mock()
        self.component.image_caption.rendered = '<p>foobar</p>'
        self.component.image.width = 1
        self.component.image.height = 2
        self.assertEqual(
            mark_safe(
                '<amp-img src="https://foo.com/foo.jpg" width="1" height="2" layout="responsive"></amp-img><div class="img-caption"><p>foobar</p></div>'
            ),
            self.renderer.amphtml,
        )

    def test_admin_string(self):
        self.assertEqual('https://foo.com/foo.jpg: very alt', self.renderer.admin_string)

    def test_string_method(self):
        self.assertEqual(
            self.renderer.alt_text,
            str(self.renderer),
        )


class PullQuoteComponentRendererTestCase(TestCase):
    def setUp(self):
        self.component = mock.Mock()
        self.component.quote = 'foo'
        self.renderer = component_renderers.PullQuoteComponentRenderer(self.component)

    def test_html(self):
        self.assertEqual(mark_safe('<blockquote aria-hidden="true">foo</blockquote>'), self.renderer.html)

    def test_admin_string(self):
        self.assertEqual(
            truncatechars(self.component.quote, component_renderers.ADMIN_FIELD_TRUNCATE_LENGTH),
            self.renderer.admin_string,
        )

    def test_string_method(self):
        self.assertEqual(
            self.component.quote,
            str(self.renderer),
        )
