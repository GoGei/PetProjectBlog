from factory import fuzzy

posts_data = {
    'title': fuzzy.FuzzyText(length=255).fuzz(),
    'heading': fuzzy.FuzzyText(length=255).fuzz(),
    'text': fuzzy.FuzzyText(length=1024).fuzz(),
}

posts_error_data = {
    'title': fuzzy.FuzzyText(length=300).fuzz(),
    'heading': fuzzy.FuzzyText(length=300).fuzz(),
    'text': fuzzy.FuzzyText(length=5000).fuzz(),
}

posts_empty_data = {
    'title': None,
    'text': None,
}

posts_filter_form_data = {
    'search': fuzzy.FuzzyText(length=10).fuzz(),
    'is_active': 'true',
    'title': fuzzy.FuzzyText(length=300).fuzz(),
    'heading': fuzzy.FuzzyText(length=300).fuzz(),
    'author': None,
}
