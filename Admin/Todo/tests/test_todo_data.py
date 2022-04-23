from factory import fuzzy


todo_data = {
    'title': fuzzy.FuzzyText(length=255).fuzz(),
    'text': fuzzy.FuzzyText(length=1024).fuzz(),
    'priority': fuzzy.FuzzyInteger(low=0).fuzz()
}

todo_error_data = {
    'title': fuzzy.FuzzyText(length=300).fuzz(),
    'text': fuzzy.FuzzyText(length=5000).fuzz(),
    'priority': fuzzy.FuzzyInteger(low=-10, high=-1).fuzz()
}

todo_empty_data = {
    'text': None,
}

todo_filter_form_data = {
    'search': fuzzy.FuzzyText(length=10).fuzz(),
    'is_active': 'true',
    'title': fuzzy.FuzzyText(length=255).fuzz(),
}
