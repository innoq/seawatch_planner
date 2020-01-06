import django_tables2 as tables
from django.utils.html import format_html, format_html_join


class CandidatesTable(tables.Table):
    id = tables.Column()
    # user = tables.Column(order_by=('user__first_name', 'user__last_name'))
    user__first_name = tables.Column()
    user__last_name = tables.Column()
    # TODO: change to approved positions?
    requested_positions = tables.ManyToManyColumn()
    availabilities = tables.ManyToManyColumn(accessor='availability_set')

    class Meta:
        template_name = "django_tables2/bootstrap4.html"

    def render_id(self, value):
        return format_html('<input type="radio" name="assignee" value="{}" />', value)

    # def render_user(self, value):
    #     return format_html("{} {}", value.first_name, value.last_name)

    def render_availabilities(self, value):
        return format_html_join("\n", "{} - {}<br>",
                                ((availability.start_date.strftime('%d.%m.%Y'),
                                  availability.end_date.strftime('%d.%m.%Y')) for availability in value.all()))
