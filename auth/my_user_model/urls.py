from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('base/',views.base,name='base'),
    path('home/',views.home, name='home'),
    path('',views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
]