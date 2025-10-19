"""
Manages the API calls for any operations related to the User

Current API Calls Handled:
    1. 
"""

from django.urls import path
import views

urlpatterns = [
    path("create", views.createUser()),
    path("login", views.loginUser()),
    path("logout", views.logoutUser()),
    path("update", views.updateUser()),
    path("info", views.getUserInfo()),
]
