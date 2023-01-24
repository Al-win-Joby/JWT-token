from django.contrib import admin
from django.urls import path,include

from . import views
urlpatterns = [
     path('',views.signup,name="signup"),
     path('login',views.login,name='login'),
     path('signedup',views.signedup,name="signedup"),
     path('loggedin',views.loggedin,name='loggedin')
]
