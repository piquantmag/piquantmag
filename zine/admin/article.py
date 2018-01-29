from django.contrib import admin
from django.utils.translation import gettext as _

import ordered_model.admin

from zine import models


@admin.register(models.Component)
class ComponentAdmin(ordered_model.admin.OrderedModelAdmin):
    fieldsets = (
        ('Article', {
            'fields': [
                'article',
            ]
        }),
        ('Component Type', {
            'fields': [
                'type',
            ]
        }),
        ('Body Component', {
            'fields': [
                'body',
            ]
        }),
        ('Image Component', {
            'fields': [
                'image',
                'image_alt_text_override',
                'image_caption',
            ]
        }),
        ('Pull Quote Component', {
            'fields': [
                'quote',
            ]
        })
    )

    list_display = ('__str__', 'type', 'article', 'move_up_down_links',)
    readonly_fields = ('move_up_down_links',)
    raw_id_fields = ('image',)


@admin.register(models.Article)
class ArticleAdmin(ordered_model.admin.OrderedModelAdmin):
    fieldsets = (
        (_('Issue Information'), {
            'fields': [
                'issue',
            ]
        }),
        (_('Article Information'), {
            'fields': [
                ('title', 'slug',),
                'synopsis',
                'authors',
                'cover_image',
            ]
        }),
        (_('History'), {
            'fields': [
                ('created_time', 'updated_time',),
            ]
        })
    )

    search_fields = [
        'title',
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
    raw_id_fields = ('cover_image',)
    save_on_top = True


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('admin_thumbnail', 'image', 'alt_text', 'height', 'width',)
    list_display = ('admin_thumbnail', 'alt_text', 'height', 'width',)
    list_editable = ('alt_text',)
    readonly_fields = ('admin_thumbnail', 'height', 'width',)
