from django.shortcuts import render
from core.User.models import User
from core.About.models import About
from core.Contacts.models import Contacts


def home_index_view(request):
    return render(request, 'Home/index.html')


def home_posts_view(request):
    superuser = User.objects.filter(is_superuser=True).first()
    posts = None
    if superuser:
        posts = superuser.posts_set.all().active().ordered()
    return render(request, 'Home/posts.html',
                  {'posts': posts})


def home_about_view(request):
    contacts = Contacts.objects.active().all()
    abouts = About.objects.active().all().order_by('order_number')
    return render(request, 'Home/about.html',
                  {'contacts': contacts,
                   'abouts': abouts})
