from django.forms import Form, ModelMultipleChoiceField, CheckboxSelectMultiple

from seawatch_registration.models import Position, Profile


class RequestedPositionForm(Form):
    requested_positions = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                                   queryset=Position.objects.all())

    class Meta:
        model = Position

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')

        super(RequestedPositionForm, self).__init__(*args, **kwargs)
        if Profile.objects.filter(user=user).exists():
            profile = Profile.objects.get(user=user)
            self.fields['requested_positions'].initial = \
                [p.pk for p in profile.requested_positions.all()]
