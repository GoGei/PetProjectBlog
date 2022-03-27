from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.TODO.models import TODOModel
from core.Utils.filtersets import BaseFilter


class TodoFilter(BaseFilter):
    SEARCH_FIELDS = ['title']

    class Meta:
        model = TODOModel
        fields = BaseFilter.BASE_FILTER_FIELDS


class TodoForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=255, required=False)
    priority = forms.IntegerField(label='Priority', min_value=0, required=False)
    text = forms.CharField(label='Text', max_length=4048, required=True,
                           widget=CKEditorUploadingWidget(config_name='admin'))

    class Meta:
        model = TODOModel
        fields = ['title', 'priority', 'text']
