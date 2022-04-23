import json
from django.test import TestCase
from core.TODO.models import TODOModel
from core.TODO.factories import TODOFactory

from ..forms import TodoForm, TodoFilter
from .test_todo_data import todo_data, todo_error_data, todo_empty_data, \
    todo_filter_form_data


class TodoFormTestCase(TestCase):
    def setUp(self):
        self.form = TodoForm

    def test_todo_form_valid(self):
        data = todo_data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_todo_form_invalid_errors(self):
        data = todo_error_data.copy()

        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_todo_form_invalid_empty(self):
        data = todo_empty_data.copy()
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class TodoFilterTestCase(TestCase):
    def setUp(self):
        self.form = TodoFilter
        self.todo = TODOFactory.create()

    def test_todo_filter_valid(self):
        data = todo_filter_form_data.copy()

        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_todo_filter_obj_found(self):
        todo = self.todo
        data = {
            'search': todo.title[:10],
        }

        form = self.form(data, queryset=TODOModel.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(todo, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(todo, form.qs)

    def test_todo_filter_obj_not_found(self):
        todo = self.todo
        data = {
            'search': todo.title[:10:-1],
        }

        form = self.form(data, queryset=TODOModel.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(todo, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertNotIn(todo, form.qs)

    def test_todo_search_success(self):
        todo = self.todo
        search_to = [todo.title[:10],
                     ]
        for search in search_to:
            data = {'search': search}
            form = self.form(data, queryset=TODOModel.objects.all())
            self.assertIn(todo, form.qs)
