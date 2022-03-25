from django.shortcuts import render, get_object_or_404
from core.User.models import User
from core.About.models import About
from core.Contacts.models import Contacts
from core.Posts.models import Posts


def home_index_view(request):
    return render(request, 'Blog/Home/index.html')


def home_posts_view(request):
    superuser = User.objects.prefetch_related('posts_set').filter(is_superuser=True).first()
    posts = None
    if superuser:
        posts = superuser.posts_set.all().active().ordered()
    return render(request, 'Blog/Posts/posts.html',
                  {'posts': posts})


def home_post_view(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    return render(request, 'Blog/Posts/post_view.html',
                  {'post': post})


def home_about_view(request):
    contacts = Contacts.objects.active().all()
    abouts = About.objects.active().all().order_by('order_number')
    return render(request, 'Blog/About/about.html',
                  {'contacts': contacts,
                   'abouts': abouts})
