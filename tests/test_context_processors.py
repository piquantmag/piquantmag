from unittest import mock

from context_processors import template_visible_settings


class TestTemplateVisibleSettings:
    def test_template_visible_settings_when_setting_exists(self, settings):
        settings.FOO = 3
        settings.TEMPLATE_VISIBLE_SETTINGS = ('FOO',)

        request = mock.Mock()
        assert template_visible_settings(request) == {'FOO': 3}

    def test_template_visible_settings_when_setting_does_not_exist(self, settings):
        settings.TEMPLATE_VISIBLE_SETTINGS = ('FOO',)

        request = mock.Mock()
        assert template_visible_settings(request) == {}
