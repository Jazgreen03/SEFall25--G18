"""
Manages Order Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from Organization.models import Organization
from Order.models import Order, OrderedItem
from Inventory.models import Inventory
import json

User = get_user_model()

@require_http_methods(["GET"])
def getAvailableItems(request: HttpRequest, orgName: str) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    user = request.user

    # Drivers can't be here
    if (user.role is "driver"):
        return JsonResponse({"details": "Driver cannot view items"}, statuscode=403)
    
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
    
    user = request.user

    if (user.role is not "user"):
        return JsonResponse({"details": "Invalid user role, cannot place order"}, statuscode=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    org = Organization.objects.get(name=data.get("organization_name"))

    if org is None:
        return JsonResponse({"details": "Organization does not exist"}, status=404)

    orderedItems = data.get("items", [])
    orgInv = org.inv

    # Create the overall Order
    order = Order.objects.create(recipient=user, associatedOrg=org)

    for oitem in orderedItems:
        itemName = oitem[0]
        itemQuantity = oitem[1]

        invItem = orgInv.get_item(itemName=itemName)
        
        if invItem is None:
            return JsonResponse({"details": "Item does not exist for Organization"}, status=404)
        
        if not isinstance(itemQuantity, int) or int(itemQuantity) > invItem.quantity:
            return JsonResponse({"details": "Quantity is invalid"}, status=404)

        # Create the OrderedItem which will link to the overall Order object
        OrderedItem.objects.create(associatedItem=invItem,associatedOrder=order)

    # Return the JSONResponse as a success with the OrderID
    return JsonResponse({"details": "Order has been placed",
                         "orderID": order.orderID}, 
                         status=201)

@require_http_methods(["GET"])
def getActiveOrders(request: HttpRequest) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
    user = request.user

    match user.role:
        case "user":
            orders = Order.objects.filter(recipient=user)
            returnOrders = []

            for order in orders:
                returnOrders.append(order.get_order_details_user())

        case "driver":
            orders = Order.objects.filter(driver=user)
            returnOrders = []

            for order in orders:
                returnOrders.append(order.get_order_details_driver())
        case "organization":
            org = Organization.objects.get(creator=user)
            orders = Order.objects.filter(associatedOrg=org.name)
            returnOrders = []

            for order in orders:
                returnOrders.append(order.get_order_details_org())

        case "admin":
            orders = Order.objects.all()
            returnOrders = []

            for order in orders:
                returnOrders.append(order.get_order_details_org())

        case _:
            return JsonResponse({"details": "Invalid Role!"}, statuscode=403)
        
    return JsonResponse({"details": "Active Orders Found",
                         "Active Orders": returnOrders}, statuscode=200)

@require_http_methods(["GET"])
def getOpenOrders(request: HttpRequest) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
    user = request.user

    if user.role is "driver":
        openOrders = Order.objects.filter(driverAssigned=False)
        allOpen = []

        for order in openOrders:
            allOpen.append(order.get_simple())

    elif user.role is "organization":
        openOrders = Order.objects.filter(status__in=[Order.StatusTypes.PLACED, Order.StatusTypes.PREPARING, Order.StatusTypes.READY])
        allOpen = []
        for order in openOrders:
            allOpen.append(order.get_order_details_org())
    
    else:
        return JsonResponse({"details": "Invalid User Role"}, statuscode=400)
    
    return JsonResponse({"details": "Open Orders Found",
                         "Orders": allOpen}, statuscode=200)
    
@require_http_methods(["PUT"])
def updateOrder(request: HttpRequest, orderID: int) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)
    
@require_http_methods(["GET"])
def getOrder(request: HttpRequest, orderID: int) -> JsonResponse:
    
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)