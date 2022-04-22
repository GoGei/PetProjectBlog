from django.conf import settings
from django.contrib import messages
from django.db.models import Case, When, BooleanField
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required

from core.TODO.models import TODOModel
from .forms import TodoFilter, TodoForm
from .tables import TodoTable


@manager_required
def todo_list_view(request):
    todo = TODOModel.objects.all()
    todo = todo.annotate(active=Case(When(archived_stamp__isnull=True, then=True),
                                     default=False, output_field=BooleanField()))
    todo = todo.order_by('-active', 'priority', '-created_stamp')

    todo_filter = TodoFilter(request.GET, queryset=todo)
    todo = todo_filter.qs
    table_body = TodoTable(todo)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'title': 'Todo Data Table',
        'body': table_body
    }
    table_filter = {
        'title': 'Todo filter',
        'body': todo_filter,
        'action': reverse('todo-list')
    }

    return render(request, 'Admin/Todo/todo_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required
def todo_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('todo-list'), host='admin')

    form_body = TodoForm(request.POST or None)

    if form_body.is_valid():
        todo = form_body.save()
        messages.success(request, f'Todo {todo.title} added')
        return redirect(reverse('todo-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }

    return render(request, 'Admin/Todo/todo_add.html',
                  {'form': form})


@manager_required
def todo_edit(request, todo_id):
    todo = get_object_or_404(TODOModel, pk=todo_id)

    if '_cancel' in request.POST:
        return redirect(reverse('todo-list'), host='admin')

    form_body = TodoForm(request.POST or None,
                         instance=todo)

    if form_body.is_valid():
        todo = form_body.save()
        todo.modify(request.user)
        messages.success(request, f'Todo {todo.title} edited')
        return redirect(reverse('todo-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }
    return render(request, 'Admin/Todo/todo_edit.html',
                  {'form': form})


@manager_required
def todo_view(request, todo_id):
    todo = get_object_or_404(TODOModel, pk=todo_id)
    return render(request, 'Admin/Todo/todo_view.html', {'todo': todo})


@manager_required
def todo_archive(request, todo_id):
    todo = get_object_or_404(TODOModel, pk=todo_id)
    todo.archive(request.user)
    messages.success(request, f'Todo {todo.title} archived')
    return redirect(reverse('todo-list'), host='admin')


@manager_required
def todo_restore(request, todo_id):
    todo = get_object_or_404(TODOModel, pk=todo_id)
    todo.restore(request.user)
    messages.success(request, f'Todo {todo.title} restored')
    return redirect(reverse('todo-list'), host='admin')


@manager_required
def todo_clear(request):
    todo = TODOModel.objects.archived()
    count = todo.count()
    todo.delete()
    messages.success(request, f'Todo successfully cleaned %s instances' % count)
    return redirect(reverse('todo-list'), host='admin')
