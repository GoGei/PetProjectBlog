import django_tables2 as tables
from core.Contacts.models import Contacts


class ContactsTable(tables.Table):
    is_active = tables.BooleanColumn(orderable=False)
    actions = tables.TemplateColumn(template_name='Admin/Contacts/contacts_actions.html', orderable=False)

    class Meta:
        model = Contacts
        fields = ('description', 'contact_info', 'field_type', 'is_active', 'actions')
        attrs = {'class': 'dataTable-table'}
        template_name = "django_tables2/bootstrap4.html"
