from django.views.generic import DetailView

from zine.models import Article


class ArticleView(DetailView):
    model = Article
