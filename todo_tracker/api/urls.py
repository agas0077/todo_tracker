# Third Party Library
from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register("tasks", views.TaskViewSet)

app_name = "api"

urlpatterns = [
    path("v1/", include(routers.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
]
