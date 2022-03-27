from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.todo_list_view, name='todo-list'),
    url(r'^add/$', views.todo_add, name='todo-add'),
    url(r'^clear/$', views.todo_clear, name='todo-clear'),
    url(r'^(?P<todo_id>\d+)/edit/$', views.todo_edit, name='todo-edit'),
    url(r'^(?P<todo_id>\d+)/view/$', views.todo_view, name='todo-view'),
    url(r'^(?P<todo_id>\d+)/archive/$', views.todo_archive, name='todo-archive'),
    url(r'^(?P<todo_id>\d+)/restore/$', views.todo_restore, name='todo-restore'),
]


