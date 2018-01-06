import logging

from django.utils import timezone
from django.views.generic import DetailView, TemplateView

from zine.models import Article, Issue


LOGGER = logging.getLogger(__name__)


class ArticleView(DetailView):
    model = Article
    slug_url_kwarg = 'article_slug'
    template_name = 'zine/article/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['issue'] = self.object.issue
        return context


class IssueView(DetailView):
    model = Issue
    slug_url_kwarg = 'issue_slug'
    template_name = 'zine/issue/view.html'

    def get_queryset(self):
        return super().get_queryset().filter(publication_date__lte=timezone.now())


class HomeView(TemplateView):
    template_name = 'zine/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            context['latest_issue'] = Issue.objects.latest('publication_date')
        except Issue.DoesNotExist:
            LOGGER.warning('There are no issues yet!')
        return context


class ManifestView(TemplateView):
    template_name = 'manifest.json'
    content_type = 'application/json'


class BrowserConfigView(TemplateView):
    template_name = 'browserconfig.xml'
    content_type = 'text/xml'
