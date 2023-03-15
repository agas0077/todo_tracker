from django.contrib import admin
from django.urls import path, include

from todo import views 

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),

]
