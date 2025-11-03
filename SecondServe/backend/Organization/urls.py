"""
Manages the API calls for any operations related to the Organization

Currently only handles Organization creation
"""

from django.urls import path
import Organization.views as views

urlpatterns = [path("", views.createOrganization)]
