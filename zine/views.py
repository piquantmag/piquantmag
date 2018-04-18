import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DetailView, TemplateView, View
from rest_framework import viewsets

from zine import models, serializers

LOGGER = logging.getLogger(__name__)


class ArticleView(DetailView):
    model = models.Article
    slug_url_kwarg = 'article_slug'
    template_name = 'zine/article/view.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            articles = models.Article.objects
        else:
            articles = models.Article.published_articles

        return (
            articles
            .select_related('issue')
            .select_related('cover_image')
            .prefetch_related('authors')
        )


class ArticlePreviewView(View):
    def get(self, request, *args, **kwargs):
        preview = get_object_or_404(models.ArticlePreview, uuid=kwargs.get('uuid'))
        article = (
            models.Article
            .objects
            .select_related('issue')
            .select_related('cover_image')
            .prefetch_related('authors')
            .get(articlepreview=preview)
        )

        if article.is_published():
            return HttpResponseRedirect(
                reverse('zine:article', kwargs={'issue_slug': article.issue.slug, 'article_slug': article.slug})
            )

        return render(
            request,
            template_name='zine/article/view.html',
            context={
                'article': article,
            }
        )


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'zine/article/edit.html',
        )

    def post(self, request, *args, **kwargs):
        return HttpResponse('Received the POST!')


@method_decorator(login_required, name='dispatch')
class ArticleEditView(View):
    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')

        return render(
            request,
            'zine/article/edit.html',
            {
                'article_id': article_id,
            }
        )

    def post(self, request, *args, **kwargs):
        return HttpResponse('Received the POST!')


class AmpArticleView(DetailView):
    model = models.Article
    slug_url_kwarg = 'article_slug'
    template_name = 'zine/article/amp.html'

    def get_queryset(self):
        return (
            models.Article
            .published_articles
            .select_related('issue')
            .select_related('cover_image')
            .prefetch_related('authors')
        )


class IssueView(DetailView):
    model = models.Issue
    slug_url_kwarg = 'issue_slug'
    template_name = 'zine/issue/view.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            issues = models.Issue.objects
        else:
            issues = models.Issue.published_issues
        return issues.prefetch_related('article_set')


class HomeView(TemplateView):
    template_name = 'zine/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        latest_issue = (
            models.Issue
            .published_issues
            .prefetch_related('article_set')
            .prefetch_related('article_set__cover_image')
            .first()
        )

        if not latest_issue:
            LOGGER.warning(_('There are no published issues. Serving the newsletter signup fallback.'))

        context['latest_issue'] = latest_issue

        return context


class ManifestView(TemplateView):
    template_name = 'manifest.json'
    content_type = 'application/json'


class BrowserConfigView(TemplateView):
    template_name = 'browserconfig.xml'
    content_type = 'text/xml'


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
