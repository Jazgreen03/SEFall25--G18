"""
Manages the API calls for any operations related to the User

Current API Calls Handled:
    1. Create User Account
    2. Login User
    3. Logout User
    4. Update User Attribute
    5. Get User Info
"""

from django.urls import path
import Organization.views as views

urlpatterns = [
    path("org/", views.createOrganization)
]
