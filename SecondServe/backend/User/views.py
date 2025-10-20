"""
Manages User Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def createUser(request: HttpRequest) -> JsonResponse:
    """
    Creates a User given the parameters provided in the HTTP Request

    On Success:
        -> Returns HTTP Response with Code 200 
        -> Saves User to Database
        -> Logs in User
    On Failure:
        -> Returns HTTP Response with Code 406 (details of response contain failing fields)

    """

    # Using the HTTP Request, parse out the information for the User object
    # being sure to check that it is valid
    return

@require_http_methods(["GET"])
def loginUser(request: HttpRequest) -> JsonResponse:
    """
    Attempts to login in a User when provided with Username/Email and a Password

    On Success:
        -> Returns HTTP Response with Code 200
        -> Logs in User
    On Failure:
        If Username/Email Unknown: Error Code 404
        If Username/Email or Password incorrect: Error Code 406

    """

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if (len(username) <= 0 and len(email) <= 0) or (len(password) <= 0):
        # Invalid Username/Password
        return JsonResponse({"details": "Must Provide Username/Email and Password"}, status=406)


    # Using the HTTP Request, parse out the information for the User object
    # being sure to check that it is valid and then attempt to log in
    return

@require_http_methods(["GET"])
def logoutUser(request: HttpRequest) -> JsonResponse:
    """
    Attempts to logout a User

    On Success:
        -> Returns HTTP Response with Code 200
        -> Logs out the User
    On Failure:
        -> Error Code 404 (If no User is logged in)

    """
    if request.user.is_authenticated:
        # Logout the user
        return
    else:
        # Throw an error
        return

@require_http_methods(["PUT"])
def updateUser(request: HttpRequest) -> JsonResponse:
    """
    Attempts to update an attribute of the User

    On Success:
        -> Returns HTTP Response with Code 200
        -> Updates User entry with "New Value" for "Attribute"
    On Failure:
        -> Error Code 404 if no User is logged in
        -> Error Code 406 if “New Value” is not acceptable for the “Attribute”
        -> Error Code 400 if attribute is “password” with an invalid “New Value”
    """

    # Attempt to update an Attribute of the User

    return

@require_http_methods(["GET"])
def getUserInfo(request: HttpRequest) -> JsonResponse:
    """
    Attempts to return basic details of a User

    On Success:
        -> Returns HTTP Response with Code 200 (Details include User info)
    On Failure:
        -> Error Code 404 if no User is logged in
    """

    # Attempt to get the details on the current User

    return