from django.conf.urls import url
from Admin.Login import views as login_views
from . import views

urlpatterns = [
    url(r'^$', views.admin_index_view, name='admin-index'),
    url(r'^login/$', login_views.admin_login_view, name='admin-login'),
    url(r'^logout/$', login_views.admin_logout_view, name='admin-logout'),
]


