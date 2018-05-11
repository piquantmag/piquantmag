from django.test import TestCase

from zine.templatetags.readtime import readtime


class ReadTimeTestCase(TestCase):
    def test_readtime_when_content_empty(self):
        self.assertEqual(0, readtime(""))

    def test_readtime_when_content_four_hundred_words(self):
        self.assertEqual('two', readtime('foo ' * 400))

    def test_readtime_when_content_two_thousand_words(self):
        self.assertEqual(10, readtime('foo ' * 2000))
