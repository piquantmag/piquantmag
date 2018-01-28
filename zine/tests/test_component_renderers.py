from unittest import mock

from django.template.defaultfilters import truncatechars
from django.test import TestCase
from django.utils.safestring import mark_safe

from zine import component_renderers


class ComponentRendererTestCase(TestCase):
    def test_base_class_is_abstract(self):
        with self.assertRaises(TypeError):
            component_renderers.ComponentRenderer('can\'t do this')


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
        self.renderer = component_renderers.ImageComponentRenderer(self.component)

    def test_alt_text_when_no_override(self):
        self.assertEqual('very alt', self.renderer.alt_text)

    def test_alt_text_when_overriden(self):
        self.component.image_alt_text_override = 'new alt'
        self.assertEqual('new alt', self.renderer.alt_text)

    def test_html(self):
        self.assertEqual(
            mark_safe('<img src="https://foo.com/foo.jpg" alt="very alt" />'),
            self.renderer.html,
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
        self.assertEqual(mark_safe('<blockquote>foo</blockquote>'), self.renderer.html)

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
