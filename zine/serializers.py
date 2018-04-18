from rest_framework import serializers

from zine import models, factories


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('pk', 'display_name',)


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = models.Image
        fields = ('pk', 'image', 'alt_text', 'height', 'width',)
        read_only_fields = ('height', 'width',)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = ('pk', 'title', 'slug', 'synopsis', 'is_published', 'created_time', 'updated_time',)


class ArticleSerializer(serializers.ModelSerializer):
    components = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = (
            'pk',
            'title',
            'slug',
            'synopsis',
            'is_published',
            'created_time',
            'updated_time',
            'components',
        )

    def get_components(self, obj):
        return [factories.ComponentRendererFactory(component).json for component in obj.component_set.all()]
