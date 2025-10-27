"""
Manages Organization Functionality, called by urls.py

Currently just used for the Creation of an Organization
"""

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from User.models import User
import json


def userHasLocationPerm(user: User) -> bool:
    """
    Checks if the Current User has the Location Role
    """
    return user.get_role() is "location"

@require_http_methods(["POST"])
def createOrganization(request: HttpRequest) -> JsonResponse:
    """
    Creates Organization Object and its associated Inventory Object
    
    """

    if userHasLocationPerm(request.user) is False:
        return JsonResponse({"details": "User has Invalid Role"}, status=401)

    if request.user.is_authenticated:
        # Create Organization
        
        # Create Inventory with associated Organization ID

        # Save to database (if not already done) and return Code 201
        
        return JsonResponse({"details": "Organization has been Created"}, status=201)

    else:
        return JsonResponse({"details": "No User is Currently Logged In"}, status=400)