# from django.shortcuts import render
from django.views.generic import TemplateView
from counter.storage import counter

class IndexView(TemplateView):
    template_name = 'counter/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['counter'] = counter.inc()
        return data
