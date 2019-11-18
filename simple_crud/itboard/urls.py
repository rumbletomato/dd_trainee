from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from itboard import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'images', views.ImageViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login/$', views.login),
    url(r'logout/$', views.logout),
    url(r'register/$', views.register),
]
