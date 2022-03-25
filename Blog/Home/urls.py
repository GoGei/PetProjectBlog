from django.conf.urls import url
from core.Posts.models import PostClassifier
from . import views

urlpatterns = [
    url(r'^$', views.home_index_view, name='home-index'),
    url(r'^about/$', views.home_about_view, name='home-about'),
    url(r'^posts/$', views.home_posts_view, name='home-posts'),
    url(r'^recently-changed-posts/$', views.home_posts_view, kwargs={'extra_filter': PostClassifier.RECENTLY_CHANGED}, name='home-recently-changed-posts'),
    url(r'^this-month-posts/$', views.home_posts_view, kwargs={'extra_filter': PostClassifier.THIS_MONTH}, name='home-this-month-posts'),
    url(r'^post/(?P<post_slug>\w+)/$', views.home_post_view, name='home-post-view'),
]
