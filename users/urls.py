"""Definiuje wzorce adresów  URL dla aplikacji users."""

from django.urls import path
from django.contrib.auth.views import LoginView							#w książce jest inaczej, w update też.

from . import views

app_name = 'users'
urlpatterns = [
    # Strona logowania.
   path('login/', LoginView.as_view(template_name='users/login.html'),  #w książce jest inaczej, w update też.
        name='login'),
   path('logout/', views.logout_view, name='logout'),
   #path('register/', views.register, name='register'),
]
