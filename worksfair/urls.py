from django.urls import path

from . import views

# app_name = 'worksfair'
urlpatterns = [
  path('', views.index, name='index'),
  path('sign-in/', views.signin, name='signin'),
  path('sign-up/', views.signin, name='signup'),
  path('login/', views.login_view, name='login'),
  path('register/', views.register_view, name='register'),
  path('logout/', views.logout_view, name='logout'),
]