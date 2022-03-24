from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.contact_list_view, name='contacts-list'),
    url(r'^add/$', views.contact_add, name='contacts-add'),
    url(r'^(?P<contact_id>\d+)/edit/$', views.contact_edit, name='contacts-edit'),
    url(r'^(?P<contact_id>\d+)/view/$', views.contact_view, name='contacts-view'),
    url(r'^(?P<contact_id>\d+)/archive/$', views.contact_archive, name='contacts-archive'),
    url(r'^(?P<contact_id>\d+)/restore/$', views.contact_restore, name='contacts-restore'),
    url(r'^(?P<contact_id>\d+)/delete/$', views.contact_delete, name='contacts-delete'),
]


