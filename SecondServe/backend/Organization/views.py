"""
Manages Organization Functionality, called by urls.py

Currently just used for the Creation of an Organization
"""

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from User.models import User
from Organization.models import Organization
import json


def userHasOrgRole(user: User) -> bool:
    """
    Checks if the Current User has the Organization Role
    """
    return user.get_role() == "organization"


@require_http_methods(["POST"])
def createOrganization(request: HttpRequest) -> JsonResponse:
    """
    Creates Organization Object and its associated Inventory Object

    """

    if request.user.is_authenticated:

        if userHasOrgRole(request.user) is False:
            return JsonResponse({"details": "User has Invalid Role"}, status=401)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"details": "Invalid JSON"}, status=400)

        # Parse the data from the request
        name = data.get("name", "")
        orgType = data.get("type", "")
        location = data.get("location", "")

        # Check if Organization already exists or if location is in use
        if (
            Organization.objects.filter(name=name).exists()
            or Organization.objects.filter(location=location).exists()
        ):
            return JsonResponse(
                {"details": "Organization Exists or Location in Use"}, status=409
            )

        # Attempt to create the Organization
        try:
            Organization.objects.createOrganization(
                user=request.user, name=name, orgType=orgType, location=location
            )
        except Exception as e:
            print(e)
            return JsonResponse({"details": "Invalid Details"}, status=404)

        # Organization Created
        return JsonResponse({"details": "Organization has been Created"}, status=201)

    else:
        return JsonResponse({"details": "No User is Currently Logged In"}, status=400)
