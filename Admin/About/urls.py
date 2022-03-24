from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.about_list_view, name='about-list'),
    url(r'^add/$', views.about_add, name='about-add'),
    url(r'^(?P<about_id>\d+)/edit/$', views.about_edit, name='about-edit'),
    url(r'^(?P<about_id>\d+)/view/$', views.about_view, name='about-view'),
    url(r'^(?P<about_id>\d+)/archive/$', views.about_archive, name='about-archive'),
    url(r'^(?P<about_id>\d+)/restore/$', views.about_restore, name='about-restore'),
    url(r'^(?P<about_id>\d+)/delete/$', views.about_delete, name='about-delete'),
]


