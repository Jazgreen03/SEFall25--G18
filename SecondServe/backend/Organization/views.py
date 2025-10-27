"""
Manages Organization Functionality, called by urls.py

Currently just used for the Creation of an Organization
"""

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
def createOrganization(request: HttpRequest) -> JsonResponse:
    """
    Creates Organization Object and its associated Inventory Object
    
    """

    # Error Checking
        # Is User logged in?
        # Does User have Location Role?

    # Create Organization

    # Create Inventory with associated Organization ID

    # Save to database (if not already done) and return Code 200