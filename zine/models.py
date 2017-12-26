from django.db import models


class Author(models.Model):
    prefixes = models.CharField(max_length=255)
    given_names = models.CharField(max_length=255)
    middle_names = models.CharField(max_length=255)
    family_names = models.CharField(max_length=255)
    suffixes = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)


class Issue(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    issue_number = models.PositiveSmallIntegerField(unique=True)
    publication_date = models.DateTimeField()


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    authors = models.ManyToManyField(Author)
    issues = models.ManyToManyField(Issue)
