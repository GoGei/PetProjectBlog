from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('Blog.Home.urls')),
]
