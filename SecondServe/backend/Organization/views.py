"""
Manages Organization Functionality, called by urls.py
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