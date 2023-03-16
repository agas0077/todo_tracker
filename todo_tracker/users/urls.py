from django.contrib.auth import views
from django.urls import path

from users.views import SignUp

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(
            template_name='users/login.html'),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path('signup/', SignUp.as_view(), name='signup')
]
