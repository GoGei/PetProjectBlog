from django.conf.urls import include, url
from Api.v1.router import router as api_router_v1


urlpatterns = [
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/', include((api_router_v1.urls, 'v1-api'), namespace='api')),
]
