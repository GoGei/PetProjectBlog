from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required

from core.Contacts.models import Contacts
from .forms import ContactsFilter, ContactsForm
from .tables import ContactsTable


@manager_required
def contact_list_view(request):
    contacts = Contacts.objects.all().ordered()

    contacts_filter = ContactsFilter(request.GET, queryset=contacts)
    contacts = contacts_filter.qs
    table_body = ContactsTable(contacts)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'title': 'Contacts Data Table',
        'body': table_body
    }
    table_filter = {
        'title': 'Contacts filter',
        'body': contacts_filter,
        'action': reverse('contacts-list')
    }

    return render(request, 'Admin/Contacts/contacts_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required
def contact_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('contacts-list'), host='admin')

    form_body = ContactsForm(request.POST or None)

    if form_body.is_valid():
        contact = form_body.save()
        messages.success(request, f'Contacts {contact.description} added')
        return redirect(reverse('contacts-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }

    return render(request, 'Admin/Contacts/contacts_add.html',
                  {'form': form})


@manager_required
def contact_edit(request, contact_id):
    contact = get_object_or_404(Contacts, pk=contact_id)

    if '_cancel' in request.POST:
        return redirect(reverse('contacts-list'), host='admin')

    form_body = ContactsForm(request.POST or None,
                             instance=contact)

    if form_body.is_valid():
        contact = form_body.save()
        contact.modify(request.user)
        messages.success(request, f'Contacts {contact.description} edited')
        return redirect(reverse('contacts-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }
    return render(request, 'Admin/Contacts/contacts_edit.html',
                  {'form': form})


@manager_required
def contact_view(request, contact_id):
    contact = get_object_or_404(Contacts, pk=contact_id)
    return render(request, 'Admin/Contacts/contacts_view.html', {'contact': contact})


@manager_required
def contact_archive(request, contact_id):
    contact = get_object_or_404(Contacts, pk=contact_id)
    contact.archive(request.user)
    messages.success(request, f'Contacts {contact.description} archived')
    return redirect(reverse('contacts-list'), host='admin')


@manager_required
def contact_restore(request, contact_id):
    contact = get_object_or_404(Contacts, pk=contact_id)
    contact.restore(request.user)
    messages.success(request, f'Contacts {contact.description} restored')
    return redirect(reverse('contacts-list'), host='admin')


@manager_required
def contact_delete(request, contact_id):
    contact = get_object_or_404(Contacts, pk=contact_id)
    contact.delete()
    messages.success(request, f'Contacts {contact.description} deleted')
    return redirect(reverse('contacts-list'), host='admin')
