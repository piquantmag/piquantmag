from django.contrib import admin

from zine import models


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = [
        'prefixes',
        'given_names',
        'middle_names',
        'family_names',
        'suffixes',
        'display_name',
    ]

    save_on_top = True
