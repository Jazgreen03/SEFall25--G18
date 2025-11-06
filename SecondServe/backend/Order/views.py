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

#################################
#   Sub-functionality Methods   #
#################################

def getOrder(request: HttpRequest, orderID: int) -> JsonResponse:
    """
    Returns role-specific information about a Placed Order
    """
    user = request.user

    order = Order.objects.get(orderID=orderID)

    match user.role:
        case "user":
            if user is not order.recipient:
                return JsonResponse({"details": "Invalid User!"}, statuscode=403)
            orderDets = order.get_order_details_user()
        case "organization":
            org = Organization.objects.get(creator=user)
            if org is None or org is not order.associatedOrg:
                return JsonResponse({"details": "Invalid User!"}, statuscode=403)
            orderDets = order.get_order_details_org()
        case "driver":
            if user is not order.driver:
                return JsonResponse({"details": "Invalid User!"}, statuscode=403)
            orderDets = order.get_order_details_driver()
        case "admin":
            orderDets = order.get_order_details_admin()
        case _:
            return JsonResponse({"details": "Invalid Role!"}, statuscode=403)

    return JsonResponse(
        {"details": "Order Retreived", "Order": orderDets}, statuscode=200
    )

def claimOrder(request: HttpRequest, orderID: int)  -> JsonResponse:

    user = request.user

    order = Order.objects.get(orderID=orderID)
    
    if user.role is not "driver":
        return JsonResponse({"details": "Invalid User!"}, statuscode=403)
    
    if order.driverAssigned:
        return JsonResponse({"details": "Order has already been claimed!"}, statuscode=403)
    
    order.driverAssigned = True
    order.driver = user

    try:
        order.full_clean()
        order.save()
        return JsonResponse({"details": "Order has been claimed"}, statuscode=200)
    except:
        return JsonResponse({"details": "Error Saving Order"}, statuscode=500)



#################################
#           API Calls           #
#################################

@require_http_methods(["GET"])
def getAvailableItems(request: HttpRequest, orgName: str) -> JsonResponse:
    """
    Returns all Items that are available to be ordered by a User
    """

    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    user = request.user

    # Drivers can't be here
    if user.role == "driver":
        return JsonResponse({"details": "Driver cannot view items"}, statuscode=403)

    org = Organization.objects.get(name=orgName)

    if org is None:
        return JsonResponse({"details": "Organization doesn't exist"}, statuscode=404)

    if user.role == "organization":
        if user != org.creator:
            return JsonResponse(
                {"details": "User is not the creator for the given organization."},
                statuscode=401,
            )

    items = org.inv.get_items()
    return JsonResponse({"items": items}, statuscode=200)


@require_http_methods(["POST"])
def placeOrder(request: HttpRequest) -> JsonResponse:
    """
    Allows a User to Place an Order, with one to many sub items
    """

    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    user = request.user

    if user.role != "user":
        return JsonResponse(
            {"details": "Invalid user role, cannot place order"}, statuscode=403
        )

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
            return JsonResponse(
                {"details": "Item does not exist for Organization"}, status=404
            )

        if not isinstance(itemQuantity, int) or int(itemQuantity) > invItem.quantity:
            return JsonResponse({"details": "Quantity is invalid"}, status=404)

        # Create the OrderedItem which will link to the overall Order object
        OrderedItem.objects.create(associatedItem=invItem, associatedOrder=order)

        # Update the organization's inventory by subtracting the numItem from the inventory
        invItem.quantity = invItem.quantity - itemQuantity
        invItem.save()

    # Return the JSONResponse as a success with the OrderID
    return JsonResponse(
        {"details": "Order has been placed", "orderID": order.orderID}, status=201
    )


@require_http_methods(["GET"])
def getActiveOrders(request: HttpRequest) -> JsonResponse:
    """
    Returns all Orders that are either active for a User, Claimed by a Driver, or Owned by an Organization
    """

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

    return JsonResponse(
        {"details": "Active Orders Found", "Active Orders": returnOrders},
        statuscode=200,
    )


@require_http_methods(["GET"])
def getOpenOrders(request: HttpRequest) -> JsonResponse:
    """
    Returns all Orders that have not been claimed by a driver, or orders that are not in transit for an Organization
    """

    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    user = request.user

    if user.role == "driver":
        openOrders = Order.objects.filter(driverAssigned=False)
        allOpen = []

        for order in openOrders:
            allOpen.append(order.get_simple())

    elif user.role == "organization":
        openOrders = Order.objects.filter(
            status__in=[
                Order.StatusTypes.PLACED,
                Order.StatusTypes.PREPARING,
                Order.StatusTypes.READY,
            ]
        )
        allOpen = []
        for order in openOrders:
            allOpen.append(order.get_order_details_org())

    else:
        return JsonResponse({"details": "Invalid User Role"}, statuscode=400)

    return JsonResponse(
        {"details": "Open Orders Found", "Orders": allOpen}, statuscode=200
    )


@require_http_methods(["PUT"])
def updateOrder(request: HttpRequest, orderID: int) -> JsonResponse:
    """
    Updates an Order status, tracking where the order is at any given time
    """

    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    user = request.user

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    # Does order exist?
    order = Order.objects.get(orderID=orderID)

    if order is None:
        return JsonResponse({"details": "Order does not exist"}, statuscode=404)

    currentStatus = order.status

    driverStatus = [order.StatusTypes.READY, order.StatusTypes.TRANSIT]
    orgStatus = [order.StatusTypes.PLACED, order.StatusTypes.PREPARING]

    if currentStatus in driverStatus and user.role != "driver":
        return JsonResponse({"details": "Invalid Role"}, statuscode=401)

    elif currentStatus in orgStatus and user.role != "organization":
        return JsonResponse({"details": "Invalid Role"}, statuscode=401)

    newStatus = data.get("status")

    if order.check_newStatus(newStatus) is False:
        return JsonResponse({"details": "Invalid New Status"}, statuscode=406)

    try:
        order.status = newStatus
        order.clean()
        order.save()
    except Exception as e:
        print(e)
        return JsonResponse({"details": "Invalid New Status"}, statuscode=406)

    return JsonResponse({"details": "Order Status Updated!"}, statuscode=200)

    
@require_http_methods(["PUT", "GET"])
def singleOrderAction(request: HttpRequest, orderID: int) -> JsonResponse:
    """
    Called when there is an action performed on a single Order Object, mainly to "get" or "claim" the Order

    Based on the request method, it is passed to the appriopate submethod accordingly

    Only accepts PUT and GET requests
    """

    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is logged in"}, statuscode=400)

    order = Order.objects.get(orderID=orderID)

    if order is None:
        return JsonResponse({"details": "Order does not exist"}, statuscode=404)
    
    # Claim Order
    if request.method is "PUT":
        return claimOrder(request, orderID)
    # Get Order
    else:
        return getOrder(request, orderID)