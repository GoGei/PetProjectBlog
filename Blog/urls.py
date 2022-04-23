from django.conf.urls import url, include
# from .views import handler401_view, handler404_view, handler500_view

urlpatterns = [
    url(r'^', include('urls')),
    url(r'', include('Blog.Home.urls')),
]

# handler401 = handler401_view
# handler404 = handler404_view
# handler500 = handler500_view
