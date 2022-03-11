from django.shortcuts import render


def index(request):
    return render(request, 'Home/index.html')


def posts(request):
    return render(request, 'Home/posts.html')


def contacts(request):
    return render(request, 'Home/contacts.html')


def about(request):
    return render(request, 'Home/about.html')
