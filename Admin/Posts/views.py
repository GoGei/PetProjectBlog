from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required

from core.Posts.models import Posts
from .forms import PostsFilter, PostForm
from .tables import PostsTable


@manager_required()
def post_list_view(request):
    posts = Posts.objects.select_related('author').all().ordered()

    posts_filter = PostsFilter(request.GET, queryset=posts)
    posts = posts_filter.qs
    table_body = PostsTable(posts)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'title': 'Posts Data Table',
        'body': table_body
    }
    table_filter = {
        'title': 'Posts filter',
        'body': posts_filter,
        'action': reverse('posts-list')
    }

    return render(request, 'Admin/Posts/posts_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required()
def post_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('posts-list'), host='admin')

    form_body = PostForm(request.POST or None,
                         author=request.user)

    if form_body.is_valid():
        post = form_body.save()
        messages.success(request, f'Post {post.title} added')
        return redirect(reverse('posts-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }

    return render(request, 'Admin/Posts/posts_add.html',
                  {'form': form})


@manager_required()
def post_edit(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)

    if '_cancel' in request.POST:
        return redirect(reverse('posts-list'), host='admin')

    form_body = PostForm(request.POST or None,
                         instance=post)

    if form_body.is_valid():
        post = form_body.save()
        post.modify(request.user)
        messages.success(request, f'Post {post.title} edited')
        return redirect(reverse('posts-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True}
    }
    return render(request, 'Admin/Posts/posts_edit.html',
                  {'form': form})


@manager_required()
def post_view(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    return render(request, 'Admin/Posts/posts_view.html', {'post': post})


@manager_required()
def post_archive(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.archive(request.user)
    messages.success(request, f'Post {post.title} archived')
    return redirect(reverse('posts-list'), host='admin')


@manager_required()
def post_restore(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.restore(request.user)
    messages.success(request, f'Post {post.title} restored')
    return redirect(reverse('posts-list'), host='admin')


@manager_required()
def post_delete(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.delete()
    messages.success(request, f'Post {post.title} deleted')
    return redirect(reverse('posts-list'), host='admin')
