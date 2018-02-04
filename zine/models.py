from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

import ordered_model.models
import markupfield.fields

from zine import factories


class Author(models.Model):
    prefixes = models.CharField(max_length=255, blank=True, null=True)
    given_names = models.CharField(max_length=255)
    middle_names = models.CharField(max_length=255, blank=True, null=True)
    family_names = models.CharField(max_length=255)
    suffixes = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name


class PublishedIssueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publication_date__lte=timezone.now())


class Issue(ordered_model.models.OrderedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    publication_date = models.DateTimeField()
    synopsis = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published_issues = PublishedIssueManager()

    class Meta(ordered_model.models.OrderedModel.Meta):
        ordering = ['order']

    def is_published(self):
        return self.publication_date <= timezone.now()
    is_published.boolean = True
    is_published.short_description = 'Published'

    def get_absolute_url(self):
        return reverse('zine:issue', kwargs={'issue_slug': self.slug})

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(height_field='height', width_field='width')
    alt_text = models.CharField(max_length=100)
    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()

    def admin_thumbnail(self):
        return mark_safe(f'<img src="{self.image.url}" height="100" />')
    admin_thumbnail.short_description = 'Thumbnail'

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'<{self.__class__.__name__} file="{self.image.name}" alt="{self.alt_text}">'


@receiver(post_delete, sender=Image)
def photograph_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(issue__publication_date__lte=timezone.now())


class Article(ordered_model.models.OrderedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    issue = models.ForeignKey(Issue, blank=True, null=True, on_delete=models.SET_NULL)
    synopsis = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField(Author, blank=True)
    cover_image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    order_with_respect_to = 'issue'

    objects = models.Manager()
    published_articles = PublishedArticleManager()

    class Meta(ordered_model.models.OrderedModel.Meta):
        ordering = ['order']

    def is_published(self):
        return self.issue and self.issue.is_published()
    is_published.boolean = True
    is_published.short_description = 'Published'

    def get_absolute_url(self):
        return reverse('zine:article', kwargs={'issue_slug': self.issue.slug, 'article_slug': self.slug})

    def __str__(self):
        return self.title

    @property
    def html(self):
        final_html = ''
        for component in self.component_set.all():
            final_html += factories.ComponentRendererFactory(component).html
        return mark_safe(final_html)

    @property
    def amphtml(self):
        final_html = ''
        for component in self.component_set.all():
            final_html += factories.ComponentRendererFactory(component).amphtml
        return mark_safe(final_html)


COMPONENT_TYPE_CHOICES = [
    ('PullQuoteComponentRenderer', 'PullQuoteComponentRenderer'),
    ('BodyComponentRenderer', 'BodyComponentRenderer'),
    ('ImageComponentRenderer', 'ImageComponentRenderer'),
]


class Component(ordered_model.models.OrderedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=COMPONENT_TYPE_CHOICES)
    body = markupfield.fields.MarkupField(markup_type='markdown', blank=True, null=True)
    quote = models.CharField(max_length=100, blank=True, null=True)
    image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE)
    image_alt_text_override = models.CharField(max_length=100, blank=True, null=True)
    image_caption = markupfield.fields.MarkupField(markup_type='markdown', blank=True, null=True)

    order_with_respect_to = ('article',)

    def __str__(self):
        return factories.ComponentRendererFactory(self).admin_string

    class Meta(ordered_model.models.OrderedModel.Meta):
        ordering = ['order']
