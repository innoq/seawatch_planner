from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic

from missions.models import DefaultAssignment, Ship


class DefaultAssignmentForm(ModelForm):

    def clean_position(self):
        position = self.cleaned_data['position']
        if self.instance.pk is None and DefaultAssignment.objects.filter(
                position=position, ship=self.initial.get('ship_id')).exists():
            raise ValidationError(_('There is already a default assignment for this position for this ship.'))
        return position

    def clean(self):
        self.instance.ship = Ship.objects.get(pk=self.initial.get('ship_id'))
        return super().clean()

    class Meta:
        model = DefaultAssignment
        fields = ('position', 'quantity')


class DefaultAssignmentBaseView(LoginRequiredMixin, PermissionRequiredMixin, generic.View):
    nav_item = 'ships'
    model = DefaultAssignment
    form_class = DefaultAssignmentForm
    permission_required = 'missions.add_defaultassignment'

    def get_success_url(self):
        ship_id = self.kwargs.get('ship_id')
        return reverse('default_assignment_list', kwargs={'ship_id': ship_id})

    def get_initial(self):
        return {'ship_id': self.kwargs.get('ship_id')}

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                'ship': get_object_or_404(Ship, pk=(self.kwargs.get('ship_id')))}


class ListView(DefaultAssignmentBaseView, generic.ListView):
    paginate_by = 10
    ordering = 'id'

    def get_queryset(self):
        ship_id = self.kwargs.get('ship_id')
        return DefaultAssignment.objects.filter(ship__id=ship_id)


class CreateView(DefaultAssignmentBaseView, generic.CreateView):
    pass


class UpdateView(DefaultAssignmentBaseView, generic.UpdateView):
    pass


class DeleteView(DefaultAssignmentBaseView, generic.DeleteView):
    pass
