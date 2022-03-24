import django_tables2 as tables
from core.About.models import About


class AboutTable(tables.Table):
    date = tables.TemplateColumn(template_name='Admin/About/about_table_date.html')
    is_active = tables.BooleanColumn()
    actions = tables.TemplateColumn(template_name='Admin/About/about_actions.html')

    class Meta:
        model = About
        fields = ('title', 'order_number', 'date', 'is_active', 'actions')
        attrs = {'class': 'dataTable-table'}
        template_name = "django_tables2/bootstrap4.html"
