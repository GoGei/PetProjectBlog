from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_index_view, name='home-index'),
    url(r'^about/$', views.home_about_view, name='home-about'),
    url(r'^posts/$', views.home_posts_view, name='home-posts'),
]
