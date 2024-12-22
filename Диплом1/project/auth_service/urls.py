from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.registration, name='register'),
    path('login/', views.login_page, name='login'),
]
