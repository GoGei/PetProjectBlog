import datetime
from factory import fuzzy

about_data = {
    'title': fuzzy.FuzzyText(length=255).fuzz(),
    'heading': fuzzy.FuzzyText(length=255).fuzz(),
    'text': fuzzy.FuzzyText(length=1024).fuzz(),
    'order_number': fuzzy.FuzzyInteger(low=0, high=100).fuzz(),

    'from_date': fuzzy.FuzzyDate(start_date=datetime.datetime.now().date() - datetime.timedelta(days=10),
                                 end_date=datetime.datetime.now().date() - datetime.timedelta(days=1)).fuzz(),
    'to_date': fuzzy.FuzzyDate(start_date=datetime.datetime.now().date()).fuzz(),
}

about_error_data = {
    'title': fuzzy.FuzzyText(length=300).fuzz(),
    'heading': fuzzy.FuzzyText(length=300).fuzz(),
    'text': fuzzy.FuzzyText(length=5000).fuzz(),
    'order_number': fuzzy.FuzzyInteger(low=-10, high=-1).fuzz(),

    'from_date': fuzzy.FuzzyDate(start_date=datetime.datetime.now().date() + datetime.timedelta(days=10),
                                 end_date=datetime.datetime.now().date() + datetime.timedelta(days=15)).fuzz(),
    'to_date': fuzzy.FuzzyDate(start_date=datetime.datetime.now().date()).fuzz(),
}

about_empty_data = {
    'title': None,
    'text': None,
}

about_filter_form_data = {
    'search': fuzzy.FuzzyText(length=10).fuzz(),
    'is_active': 'true',
    'from_date': fuzzy.FuzzyDate(start_date=datetime.datetime.now().date() - datetime.timedelta(days=10),
                                 end_date=datetime.datetime.now().date() - datetime.timedelta(days=1)).fuzz(),
    'to_date': fuzzy.FuzzyDate(start_date=datetime.datetime.now().date()).fuzz(),
}
