from zine.templatetags.readtime import readtime


def test_readtime_when_content_empty():
    assert readtime("") == 0

def test_readtime_when_content_four_hundred_words():
    assert readtime('foo ' * 400) == 'two'

def test_readtime_when_content_two_thousand_words():
    assert readtime('foo ' * 2000) == 10
