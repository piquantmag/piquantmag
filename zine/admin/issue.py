from django.contrib import admin
from django.utils.translation import gettext as _

import ordered_model.admin

from zine import models


@admin.register(models.Issue)
class IssueAdmin(ordered_model.admin.OrderedModelAdmin):
    fieldsets = (
        (_('Issue Information'), {
            'fields': [
                ('title', 'slug',),
                'synopsis',
            ],
        }),
        (_('Cover Image'), {
            'fields': [
                'cover_image',
            ],
        }),
        (_('Publication Information'), {
            'fields': [
                'publication_date',
            ],
        }),
        (_('History'), {
            'fields': [
                ('created_time', 'updated_time',),
            ],
        })
    )

    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)
    list_display = ('title', 'move_up_down_links', 'is_published',)
    date_hierarchy = 'publication_date'
    search_fields = ('title',)
    raw_id_fields = ('cover_image',)
    readonly_fields = ('created_time', 'updated_time',)
    save_on_top = True
