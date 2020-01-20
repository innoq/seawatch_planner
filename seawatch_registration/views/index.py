from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    nav_item = 'index'
    template_name = 'index.html'
