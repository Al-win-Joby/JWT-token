from django.contrib import admin
from django.urls import path,include
from .views import RegisterView,LoginView,UserViews,LogoutViews
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserViews.as_view()),
    path('logout',LogoutViews.as_view()),
]
