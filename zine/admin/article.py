from django.contrib import admin

import ordered_model.admin

from zine import models


@admin.register(models.Article)
class ArticleAdmin(ordered_model.admin.OrderedModelAdmin):
    fieldsets = (
        ('Issue Information', {
            'fields': [
                'issue',
            ]
        }),
        ('Article Information', {
            'fields': [
                ('title', 'slug',),
                'authors',
                'body',
                'synopsis',
            ]
        }),
        ('History', {
            'fields': [
                ('created_time', 'updated_time',),
            ]
        })
    )

    search_fields = [
        'title',
        'body',
    ]

    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-issue__order', 'order']
    list_display = ('title', 'issue', 'move_up_down_links', 'is_published',)
    list_display_links = ('title',)
    list_select_related = ('issue',)
    date_hierarchy = 'issue__publication_date'
    filter_horizontal = ('authors',)
    autocomplete_fields = ('issue',)
    readonly_fields = ('created_time', 'updated_time',)
    save_on_top = True
