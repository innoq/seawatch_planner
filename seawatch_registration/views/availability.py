import django.views.generic as generic
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse

from seawatch_registration.models import Profile, Availability
from seawatch_registration.widgets import DateInput, DatePickerInput


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Availability
    fields = ['start_date', 'end_date', 'comment']
    nav_item = 'availabilities'
    submit_button = 'Add'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('availability_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = DateInput()
        form.fields['end_date'].widget = DateInput()
        return form


class ListView(LoginRequiredMixin, UserPassesTestMixin, generic.View):

    nav_item = 'availabilities'
    title = 'Availabilities'
    success_alert = 'Available Dates successfully saved!'
    submit_button = 'Save'
    template_name = './seawatch_registration/availability_list.html'

    AvailableDatesFormset = inlineformset_factory(Profile,
                                                  Availability,
                                                  fields=('start_date', 'end_date', 'comment'),
                                                  widgets={
                                                    'start_date': DatePickerInput(),
                                                    'end_date': DatePickerInput()},
                                                  extra=0, max_num=4, min_num=1,
                                                  can_delete=True)

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        formset = self.AvailableDatesFormset(instance=profile)
        return render(request, self.template_name,
                      {'formset': formset,
                       'view': self
                       })

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        formset = self.AvailableDatesFormset(request.POST, instance=profile)
        error_msg = 'Input could not be saved. Please correct missing or invalid data!'
        if not formset.is_valid():      
            return render(request, self.template_name,
                          {'formset': formset,
                           'view': self,
                           'error': error_msg,
                           })

        formset.save()

        formset = self.AvailableDatesFormset(instance=profile)
        return render(request, self.template_name,
                      {'formset': formset,
                       'view': self
                       })

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
