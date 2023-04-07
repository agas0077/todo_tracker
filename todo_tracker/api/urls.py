from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

routers = DefaultRouter()
routers.register('tasks', views.TaskViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/', include(routers.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
