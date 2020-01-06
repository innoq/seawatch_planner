from django.shortcuts import render
from django.views.generic.base import ContextMixin, View


class IndexView(View, ContextMixin):
    nav_item = 'index'

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context=self.get_context_data())
