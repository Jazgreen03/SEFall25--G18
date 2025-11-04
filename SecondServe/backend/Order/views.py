"""
Manages Order Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def getAvailableItems(request: HttpRequest) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
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