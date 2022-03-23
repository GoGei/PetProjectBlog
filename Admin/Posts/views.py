from django.conf import settings
from django.shortcuts import render, redirect, reverse
from core.Utils.Access.decorators import manager_required

from .tables import PostsTable
from core.Posts.models import Posts


@manager_required()
def post_list_view(request):
    posts = Posts.objects.all().ordered()
    table = PostsTable(posts)
    page = request.GET.get("page", 1)
    table.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)
    return render(request, 'Admin/Posts/posts_list.html',
                  {'table': table})


@manager_required()
def post_list_add(request):
    return render(request, 'Admin/Posts/posts_add.html')


@manager_required()
def post_list_edit(request, post_id):
    return render(request, 'Admin/Posts/posts_edit.html')


@manager_required()
def post_list_archive(request, post_id):
    return redirect(reverse('posts-list'), host='admin')


@manager_required()
def post_list_restore(request, post_id):
    return redirect(reverse('posts-list'), host='admin')


@manager_required()
def post_list_delete(request, post_id):
    return redirect(reverse('posts-list'), host='admin')
