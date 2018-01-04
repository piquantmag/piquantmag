from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import ordered_model.models
import markupfield.fields


class Author(models.Model):
    prefixes = models.CharField(max_length=255, blank=True, null=True)
    given_names = models.CharField(max_length=255)
    middle_names = models.CharField(max_length=255, blank=True, null=True)
    family_names = models.CharField(max_length=255)
    suffixes = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name


class Issue(ordered_model.models.OrderedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    publication_date = models.DateTimeField()
    synopsis = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta(ordered_model.models.OrderedModel.Meta):
        ordering = ['order']

    def is_published(self):
        return self.publication_date <= timezone.now()
    is_published.boolean = True
    is_published.short_description = 'Published'

    def get_absolute_url(self):
        return reverse('zine:issue', kwargs={'issue_slug': self.slug})

    @property
    def issue_number(self):
        all_issues = [issue for issue in Issue.objects.all()]
        return all_issues.index(self) + 1

    def __str__(self):
        return _('Issue') + f' {self.issue_number}: {self.title}'


class Article(ordered_model.models.OrderedModel):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField(Author)
    issue = models.ForeignKey(Issue, blank=True, null=True, on_delete=models.SET_NULL)
    body = markupfield.fields.MarkupField(markup_type='markdown')
    order_with_respect_to = 'issue'
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

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
