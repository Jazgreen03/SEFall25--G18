"""
Manages Inventory Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from User.models import User
from Organization.models import Organization, OrganizationManager
from Inventory.models import Inventory


def checkUser(user: User) -> JsonResponse | None:    
    """
    Checks is a User is Logged In and if they have the Location Permission.

    Success is assumed if the method returns nothing
    """
    if user.is_authenticated is False:
        return JsonResponse({"details": "No User is Currently Logged In"}, status=400)
    
    if (user.get_role() is "location") is False:
        return JsonResponse({"details": "User has Invalid Role"}, status=401)

def getInventory(user: User) -> Inventory:
    org = Organization.objects.filter(creator=user).first()

    if org is None:
        return JsonResponse({"details": "User is not associated with Organization"}, status=404)
    
    inv = Inventory.objects.filter(organization=org.name).first()

    return inv

# Get Inventory
@require_http_methods(["GET"])
def get_inventory(request: HttpRequest) -> JsonResponse:
    
    response = checkUser(request.user)

    if response is not None:
        return response

    # Get the Inventory
    inv = get_inventory(request.user)

    items = list(inv.items.values('name', 'type', 'quantity', 'expiration', 'added', 'lastUpdated'))

    return JsonResponse({"inventory": items}, status=200)



# Add Item to Inventory
@require_http_methods(["POST"])
def add_to_inventory(request: HttpRequest) -> JsonResponse:
    
    checkUser(request.user)

    # Get the Inventory
    inv = get_inventory(request.user)

    # Parse the parameters

# Update Inventory
@require_http_methods(["PUT"])
def update_inventory(request: HttpRequest) -> JsonResponse:
    
    checkUser(request.user)

    # Get the Inventory
    inv = get_inventory(request.user)

# Edit Item
@require_http_methods(["PUT"])
def edit_inventory(request: HttpRequest) -> JsonResponse:
    
    checkUser(request.user)

    # Get the Inventory
    inv = get_inventory(request.user)