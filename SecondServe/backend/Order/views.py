"""
Manages Order Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from Organization.models import Organization
import json

User = get_user_model()

@require_http_methods(["GET"])
def getAvailableItems(request: HttpRequest, orgName: str) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    user = request.user

    # Drivers can't be here
    if (user.role is "driver"):
        return JsonResponse({"details": "Driver cannot view items"}, statuscode=404)
    
    org = Organization.objects.get(name=orgName)

    if (user.role is "organization"):

        if (user is not org.creator):
            return JsonResponse({"details": "User is not the creator for the given organization."}, statuscode=401)

    items = org.inv.get_items()
    return JsonResponse({"items": items}, statuscode=200)
        
    
    
@require_http_methods(["POST"])
def placeOrder(request: HttpRequest) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
@require_http_methods(["GET"])
def getActiveOrders(request: HttpRequest) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
@require_http_methods(["GET"])
def getOpenOrders(request: HttpRequest) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
@require_http_methods(["PUT"])
def updateOrder(request: HttpRequest, orderID: int) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
@require_http_methods(["GET"])
def getOrder(request: HttpRequest, orderID: int) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)