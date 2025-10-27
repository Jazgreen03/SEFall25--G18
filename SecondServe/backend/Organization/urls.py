"""
Manages the API calls for any operations related to the Organization

Currently, the only API Call handled is for the creation of an Organization
"""

from django.urls import path
import Organization.views as views

urlpatterns = [
    path("org/", views.createOrganization)
]
