from django.urls import path

from todo import views

app_name = 'todo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('<int:task_id>/update_task/', views.update_task, name='update_task'),
    path('<int:task_id>/delete_task/', views.delete_task, name='delete_task'),
    path('congrats/', views.congrats, name='congrats'),
]
