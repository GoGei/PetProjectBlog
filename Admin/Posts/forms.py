import django_filters
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.Posts.models import Posts
from core.User.models import User
from core.Utils.filtersets import BaseFilter


class PostsFilter(BaseFilter):
    SEARCH_FIELDS = ['title', 'heading', 'author__email']

    author = django_filters.ModelChoiceFilter(queryset=User.objects.filter(is_active=True).all(),
                                              empty_label='Not selected')

    class Meta:
        model = Posts
        fields = BaseFilter.BASE_FILTER_FIELDS


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=255, required=True)
    heading = forms.CharField(label='Heading', max_length=255, required=False)
    text = forms.CharField(label='Text', max_length=4048, required=True,
                           widget=CKEditorUploadingWidget(config_name='admin'))

    class Meta:
        model = Posts
        fields = ['title', 'heading', 'text']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        if title and not self.Meta.model.is_allowed_to_assign_slug(instance=self.instance, title=title):
            self.add_error('title', 'This title generates slug, that is already exists! Please, change it.')
        return title

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)

        if self.author:
            instance.author = self.author

        instance.assign_slug()
        if commit:
            instance.save()
        return instance
