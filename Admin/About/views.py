from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required

from core.About.models import About
from .forms import AboutFilter, AboutForm
from .tables import AboutTable


@manager_required
def about_list_view(request):
    about = About.objects.all().ordered()

    about_filter = AboutFilter(request.GET, queryset=about)
    about = about_filter.qs
    table_body = AboutTable(about)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'title': 'About Data Table',
        'body': table_body
    }
    table_filter = {
        'title': 'About filter',
        'body': about_filter,
        'action': reverse('about-list')
    }

    return render(request, 'Admin/About/about_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required
def about_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('about-list'), host='admin')

    form_body = AboutForm(request.POST or None)

    if form_body.is_valid():
        about = form_body.save()
        messages.success(request, f'About {about.title} added')
        return redirect(reverse('about-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }

    return render(request, 'Admin/About/about_add.html',
                  {'form': form})


@manager_required
def about_edit(request, about_id):
    about = get_object_or_404(About, pk=about_id)

    if '_cancel' in request.POST:
        return redirect(reverse('about-list'), host='admin')

    form_body = AboutForm(request.POST or None,
                          instance=about)

    if form_body.is_valid():
        about = form_body.save()
        about.modify(request.user)
        messages.success(request, f'About {about.title} edited')
        return redirect(reverse('about-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }
    return render(request, 'Admin/About/about_edit.html',
                  {'form': form})


@manager_required
def about_view(request, about_id):
    about = get_object_or_404(About, pk=about_id)
    return render(request, 'Admin/About/about_view.html', {'about': about})


@manager_required
def about_archive(request, about_id):
    about = get_object_or_404(About, pk=about_id)
    about.archive(request.user)
    messages.success(request, f'About {about.title} archived')
    return redirect(reverse('about-list'), host='admin')


@manager_required
def about_restore(request, about_id):
    about = get_object_or_404(About, pk=about_id)
    about.restore(request.user)
    messages.success(request, f'About {about.title} restored')
    return redirect(reverse('about-list'), host='admin')


@manager_required
def about_delete(request, about_id):
    about = get_object_or_404(About, pk=about_id)
    about.delete()
    messages.success(request, f'About {about.title} deleted')
    return redirect(reverse('about-list'), host='admin')
