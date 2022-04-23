import json
from django.test import TestCase
from core.Posts.models import Posts
from core.Posts.factories import PostsFactory
from core.User.factories import UserFactory

from ..forms import PostForm, PostsFilter
from .test_posts_data import posts_data, posts_error_data, posts_empty_data, \
    posts_filter_form_data


class PostsFormTestCase(TestCase):
    def setUp(self):
        self.form = PostForm
        self.kwargs = {'author': UserFactory.create()}

    def test_posts_form_valid(self):
        data = posts_data.copy()
        form = self.form(data, **self.kwargs)
        self.assertTrue(form.is_valid())

    def test_posts_form_invalid_errors(self):
        data = posts_error_data.copy()
        form = self.form(data, **self.kwargs)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_posts_form_invalid_empty(self):
        data = posts_empty_data.copy()
        form = self.form(data, **self.kwargs)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class PostsFilterTestCase(TestCase):
    def setUp(self):
        self.form = PostsFilter
        self.post = PostsFactory.create()

    def test_posts_filter_valid(self):
        data = posts_filter_form_data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_posts_filter_obj_found(self):
        post = self.post
        data = {
            'search': post.title[:10],
            'author': post.author
        }
        form = self.form(data, queryset=Posts.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(post, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(post, form.qs)

    def test_posts_filter_obj_not_found(self):
        post = self.post
        data = {
            'search': post.title[:10:-1],
        }
        form = self.form(data, queryset=Posts.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(post, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertNotIn(post, form.qs)

    def test_posts_search_success(self):
        post = self.post
        search_to = [post.title[:10],
                     post.heading[:10],
                     post.author.email[:10]]
        for search in search_to:
            data = {'search': search}
            form = self.form(data, queryset=Posts.objects.all())
            self.assertIn(post, form.qs)
