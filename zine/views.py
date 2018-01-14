import logging

from django.views.generic import DetailView, TemplateView

from zine.models import Article, Issue


LOGGER = logging.getLogger(__name__)


class ArticleView(DetailView):
    model = Article
    slug_url_kwarg = 'article_slug'
    template_name = 'zine/article/view.html'

    def get_queryset(self):
        return Article.published_articles.select_related('issue')


class IssueView(DetailView):
    model = Issue
    slug_url_kwarg = 'issue_slug'
    template_name = 'zine/issue/view.html'

    def get_queryset(self):
        return Issue.published_issues.prefetch_related('article_set')


class HomeView(TemplateView):
    template_name = 'zine/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        latest_issue = (
            Issue
            .published_issues
            .prefetch_related('article_set')
            .first()
        )

        if not latest_issue:
            LOGGER.warning('There are no published issues. Serving the newsletter signup fallback.')

        context['latest_issue'] = latest_issue

        return context


class ManifestView(TemplateView):
    template_name = 'manifest.json'
    content_type = 'application/json'


class BrowserConfigView(TemplateView):
    template_name = 'browserconfig.xml'
    content_type = 'text/xml'
