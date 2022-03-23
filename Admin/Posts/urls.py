from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list_view, name='posts-list'),
    url(r'^add/$', views.post_list_add, name='posts-add'),
    url(r'^(?P<post_id>\d+)/edit/$', views.post_list_edit, name='posts-edit'),
    url(r'^(?P<post_id>\d+)/archive/$', views.post_list_archive, name='posts-archive'),
    url(r'^(?P<post_id>\d+)/restore/$', views.post_list_restore, name='posts-restore'),
    url(r'^(?P<post_id>\d+)/delete/$', views.post_list_delete, name='posts-delete'),
]


