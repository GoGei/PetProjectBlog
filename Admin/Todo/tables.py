import django_tables2 as tables
from core.About.models import About


class TodoTable(tables.Table):
    is_active = tables.BooleanColumn(orderable=False)
    actions = tables.TemplateColumn(template_name='Admin/Todo/todo_actions.html', orderable=False)

    class Meta:
        model = About
        fields = ('title', 'is_active', 'actions')
        attrs = {'class': 'dataTable-table'}
        template_name = "django_tables2/bootstrap4.html"
