from abc import ABCMeta, abstractmethod

from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe


ADMIN_FIELD_TRUNCATE_LENGTH = 40


class ComponentRenderer(metaclass=ABCMeta):
    def __init__(self, component):
        self.component = component

    @property
    @abstractmethod
    def html(self):
        pass

    @property
    @abstractmethod
    def admin_string(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class BodyComponentRenderer(ComponentRenderer):
    @property
    def html(self):
        return mark_safe(self.component.body.rendered)

    @property
    def admin_string(self):
        return truncatechars(self.component.body.raw, ADMIN_FIELD_TRUNCATE_LENGTH)

    def __str__(self):
        return self.component.body.raw


class PullQuoteComponentRenderer(ComponentRenderer):
    @property
    def html(self):
        return mark_safe(f'<blockquote>{self.component.quote}</blockquote>')

    @property
    def admin_string(self):
        return truncatechars(self.component.quote, ADMIN_FIELD_TRUNCATE_LENGTH)

    def __str__(self):
        return self.component.quote


class ImageComponentRenderer(ComponentRenderer):
    @property
    def html(self):
        return mark_safe(f'<img src="{self.component.image.image.url}" alt="{self.alt_text}" />')

    @property
    def admin_string(self):
        return f'{self.component.image.image.url}: {self.alt_text}'

    @property
    def alt_text(self):
        return self.component.image_alt_text_override or self.component.image.alt_text

    def __str__(self):
        return self.alt_text
