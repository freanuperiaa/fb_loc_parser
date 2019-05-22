from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.core import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('api/', include('apps.core.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
