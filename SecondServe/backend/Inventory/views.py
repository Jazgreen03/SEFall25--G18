"""
Manages Inventory Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from User.models import User
from Organization.models import Organization
from Inventory.models import Inventory, Item
import json
from datetime import datetime

#################################################
#               Helper Methods                  #
#################################################


def checkUser(user: User) -> JsonResponse | None:
    """
    Checks is a User is Logged In and if they have the Location Permission.

    Success is assumed if the method returns nothing
    """
    if user.is_authenticated is False:
        return JsonResponse({"details": "No User is Currently Logged In"}, status=400)

    if (user.get_role() == "location") is False:
        return JsonResponse({"details": "User has Invalid Role"}, status=401)

    if Organization.objects.filter(creator=user).first() is None:
        return JsonResponse(
            {"details": "User is not associated with Organization"}, status=404
        )


def getInv(user: User) -> Inventory:
    """
    Returns the Inventory for the Organization that the User is affilated with
    """
    org = Organization.objects.filter(creator=user).first()

    inv = Inventory.objects.filter(org=org.name).first()

    return inv


def editItem(attr: str, val: str, item: Item) -> JsonResponse | None:
    """
    Edits a single Attribute of a given Item with a new Value
    """

    updatedAttr = ""

    match attr:
        case "name":
            updatedAttr = "name"
            item.name = val
        case "type":
            updatedAttr = "type"
            item.type = val
        case "quantity":
            updatedAttr = "quantity"
            try:
                quantity = int(val)
                item.quantity = quantity
            except Exception as e:
                print(e)
                return JsonResponse({"details": "Invalid Attribute Passed"}, status=406)
        case "expiration":
            updatedAttr = "expiration"
            eDate = datetime.strptime(val, "%B %d, %Y").date()
            item.expiration = eDate
        case _:
            return JsonResponse({"details": "Invalid Attribute Passed"}, status=406)

    try:
        item.full_clean()
        item.save(update_fields=[updatedAttr])
    except Exception as e:
        print(e)
        # Don't save the item cause its wrong
        return JsonResponse({"details": "Invalid Parameter Values"}, status=406)


#################################################
#                   API Methods                 #
#################################################


# Get Inventory
@require_http_methods(["GET"])
def get_inventory(request: HttpRequest) -> JsonResponse:

    response = checkUser(request.user)

    if response is not None:
        return response

    # Get the Inventory
    inv = getInv(request.user)

    items = inv.get_items()

    items_return = [item.to_dict() for item in items]

    return JsonResponse({"inventory": items_return}, status=200)


# Add Item to Inventory
@require_http_methods(["POST"])
def add_to_inventory(request: HttpRequest) -> JsonResponse:

    response = checkUser(request.user)

    if response is not None:
        return response

    # Get the Inventory
    inv = getInv(request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    # Parse the parameters
    itemName = data.get("item_name")
    itemQuantity = data.get("quantity")
    itemExpiration = data.get("expiration")
    itemType = data.get("type")

    # Check that all arguments were passed properly
    if (
        itemName is None
        or itemExpiration is None
        or itemQuantity is None
        or itemType is None
    ):
        return JsonResponse(
            {"details": "Must provide valid parameters for Item"}, status=404
        )

    # Check if the Item already exists
    if inv.has_item(itemName):
        return JsonResponse({"details": "Item already exists in inventory"}, status=409)

    # Attempt to create the Item
    try:
        # Convert the expiration date to the proper format
        eDate = datetime.strptime(itemExpiration, "%B %d, %Y").date()
        Item.objects.create(
            name=itemName,
            quantity=itemQuantity,
            expiration=eDate,
            type=itemType,
            inventory=inv,
        )
    except Exception as e:
        print(e)
        return JsonResponse({"details": "Invalid Parameter Values"}, status=404)

    return JsonResponse({"details": "Item created successfully!"}, status=201)


# Update Inventory (Bulk Edit)
@require_http_methods(["PUT"])
def update_inventory(request: HttpRequest) -> JsonResponse:

    response = checkUser(request.user)

    if response is not None:
        return response

    # Get the Inventory
    inv = getInv(request.user)

    # Parse the parameters from the request
    try:
        data = json.loads(request.body)
        items = data.get("items", [])
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    for item in items:
        item_name = item.get("item_name", None)
        attributes = item.get("attributes", [])
        values = item.get("values", [])

        # Check that the attribute and value arrays match
        if item_name is None or len(attributes) != len(values):
            return JsonResponse({"details": "Invalid Parameter Values"}, status=406)

        # Check if the item exists in the inventory
        if inv.has_item(itemName=item_name) is False:
            return JsonResponse(
                {"details": "Item (" + item_name + ") does not exist"}, status=404
            )

        # Get the item from the inventory
        currentItem = inv.get_item(itemName=item_name)

        # Iterate through all the attributes/values updating the item as we go
        for attr, val in zip(attributes, values):
            # This edits and saves the item for each valid attribute/value
            # Is this a bad idea? Probably, but its for a future Twiggy or dev
            # to fix.
            response = editItem(attr, val, currentItem)
            if response is not None:
                return response

    # End of item iteration
    return JsonResponse({"details": "Items Updated!"}, status=200)


# Edit Item
@require_http_methods(["PUT"])
def edit_inventory(request: HttpRequest) -> JsonResponse:

    response = checkUser(request.user)

    if response is not None:
        return response

    # Get the Inventory
    inv = getInv(request.user)

    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    item_name = data.get("item_name", None)
    attributes = data.get("attributes", [])
    values = data.get("values", [])

    # Check that the attribute and value arrays match
    if item_name is None or len(attributes) != len(values):
        return JsonResponse({"details": "Invalid Parameter Values"}, status=406)

    # Check if the item exists in the inventory
    if inv.has_item(itemName=item_name) is False:
        return JsonResponse(
            {"details": "Item (" + item_name + ") does not exist"}, status=404
        )

    currentItem = inv.get_item(itemName=item_name)

    # Iterate through all the attributes/values updating the item as we go
    for attr, val in zip(attributes, values):
        # This edits and saves the item for each valid attribute/value
        # Is this a bad idea? Probably, but its for a future Twiggy or dev
        # to fix.
        response = editItem(attr, val, currentItem)
        if response is not None:
            return response

    return JsonResponse({"details": "Item Edited!"}, status=200)
