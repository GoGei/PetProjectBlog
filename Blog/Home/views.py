from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from core.User.models import User
from core.About.models import About
from core.Contacts.models import Contacts
from core.Posts.models import Posts
from .forms import PostOrderClass, PostExtraFilterClass


def home_index_view(request):
    return render(request, 'Blog/Home/index.html')


def home_posts_view(request, extra_filter=None):
    superuser = User.objects.prefetch_related('posts_set').filter(is_superuser=True).first()
    posts = None
    if superuser:
        posts = superuser.posts_set.all().active()

    if posts:
        extra_filter_class = PostExtraFilterClass(extra_filter=extra_filter, qs=posts)
        posts = extra_filter_class.get_qs()

        order_class = PostOrderClass(request=request, qs=posts)
        posts = order_class.get_qs()

        page = request.GET.get('page')
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        posts = paginator.get_page(page)

    return render(request, 'Blog/Posts/posts.html',
                  {'posts': posts})


def home_post_view(request, post_slug):
    post = get_object_or_404(Posts, slug=post_slug)
    return render(request, 'Blog/Posts/post_view.html',
                  {'post': post})


def home_about_view(request):
    contacts = Contacts.objects.active().all()
    abouts = About.objects.active().all().order_by('order_number')
    return render(request, 'Blog/About/about.html',
                  {'contacts': contacts,
                   'abouts': abouts})
