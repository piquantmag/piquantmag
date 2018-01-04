from django.utils import timezone
from django.views.generic import DetailView

from zine.models import Article, Issue


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
