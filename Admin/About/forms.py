import django_filters
from django import forms

from core.About.models import About
from core.Utils.filtersets import BaseFilter


class AboutFilter(BaseFilter):
    SEARCH_FIELDS = ['title']
    from_date = django_filters.DateFilter(label='From', required=False, method='from_date_filter',
                                          widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = django_filters.DateFilter(label='To', required=False, method='to_date_filter',
                                        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = About
        fields = ['from_date', 'to_date'] + BaseFilter.BASE_FILTER_FIELDS

    def from_date_filter(self, queryset, name, value):
        queryset = queryset.filter(from_date__gte=value)
        return queryset

    def to_date_filter(self, queryset, name, value):
        queryset = queryset.filter(to_date__lte=value)
        return queryset


class AboutForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=255, required=True)
    heading = forms.CharField(label='Heading', max_length=255, required=False)
    text = forms.CharField(label='Text', max_length=4048, required=True,
                           widget=forms.Textarea())
    order_number = forms.IntegerField(label='Order number', min_value=0, required=False)
    from_date = forms.DateField(label='From', required=False,
                                widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label='To', required=False,
                              widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = About
        fields = ['title', 'heading', 'text', 'order_number', 'from_date', 'to_date']

    def clean(self):
        cleaned_data = self.cleaned_data
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            self.add_error('from_date', '"From" date can not be more then "To" date')
            self.add_error('to_date', '"To" date can not be less then "From" date')

        return cleaned_data
