from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home-index'),
    url(r'^contacts/$', views.contacts, name='home-contacts'),
    url(r'^about/$', views.about, name='home-about'),
    url(r'^posts/$', views.posts, name='home-posts'),
]
