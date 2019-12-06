from django.urls import reverse
from django.forms.models import modelform_factory


class GetSuccessUrlFromUrlMixin(object):
    def get_success_url(self):
        redirect_to = self.request.GET.get('next')
        if redirect_to:
            return reverse(redirect_to)

        return self.success_url


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)
