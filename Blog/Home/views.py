from django.shortcuts import render


def home_index_view(request):
    return render(request, 'Home/index.html')


def home_posts_view(request):
    posts = range(5)
    return render(request, 'Home/posts.html',
                  {'posts': posts})


def home_about_view(request):
    abouts = range(5)
    contacts = range(5)
    return render(request, 'Home/about.html',
                  {'contacts': contacts,
                   'abouts': abouts})
