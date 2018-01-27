from unittest import mock

from django.test import TestCase, override_settings

from context_processors import template_visible_settings


class TemplateVisibleSettingsTestCase(TestCase):
    def test_template_visible_settings_when_setting_exists(self):
        request = mock.Mock()
        with override_settings(TEMPLATE_VISIBLE_SETTINGS=['FOO'], FOO=3):
            self.assertDictEqual({'FOO': 3}, template_visible_settings(request))

    def test_template_visible_settings_when_setting_does_not_exist(self):
        request = mock.Mock()
        with override_settings(TEMPLATE_VISIBLE_SETTINGS=['FOO']):
            self.assertDictEqual({}, template_visible_settings(request))
