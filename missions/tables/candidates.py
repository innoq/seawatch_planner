import django_tables2 as tables
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html, format_html_join


class CandidatesTable(tables.Table):
    id = tables.Column(verbose_name='', orderable=False)
    user = tables.Column(order_by=('user__first_name', 'user__last_name'))
    requested_positions = tables.ManyToManyColumn()
    approved_positions = tables.ManyToManyColumn()
    availabilities = tables.ManyToManyColumn(accessor='availability_set')

    class Meta:
        template_name = "django_tables2/bootstrap4.html"

    def render_id(self, value: int):
        return format_html('<input {} type="radio" name="assignee" value="{}" />',
                           'checked' if self.selected_user and self.selected_user.profile.id == value else '', value)

    def render_user(self, value: User):
        return format_html('<a href="{}">{} {}</a>',
                           reverse('assessment_update', kwargs={'pk': value.profile.assessment_set.first().pk}),
                           value.first_name, value.last_name)

    def render_availabilities(self, value: QuerySet):
        return format_html_join("\n", "{} - {}<br>",
                                ((availability.start_date.strftime('%d.%m.%Y'),
                                  availability.end_date.strftime('%d.%m.%Y')) for availability in value.all()))

    def __init__(self, selected_user=None, **kwargs):
        self.selected_user = selected_user
        super().__init__(**kwargs)
