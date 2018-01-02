from django.contrib import admin

import ordered_model.admin

from zine import models


@admin.register(models.Issue)
class IssueAdmin(ordered_model.admin.OrderedModelAdmin):
    fieldsets = (
        ('Issue Information', {
            'fields': [
                ('title', 'slug',),
                'synopsis',
            ]
        }),
        ('Publication Information', {
            'fields': [
                'publication_date',
            ]
        }),
        ('History', {
            'fields': [
                ('created_time', 'updated_time',),
            ]
        })
    )

    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)
    list_display = ('title', 'move_up_down_links', 'is_published',)
    date_hierarchy = 'publication_date'
    search_fields = ('title',)
    readonly_fields = ('created_time', 'updated_time',)
    save_on_top = True
