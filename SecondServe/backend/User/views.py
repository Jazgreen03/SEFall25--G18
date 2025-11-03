"""
Manages User Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()

@require_http_methods(["POST"])
def createUser(request: HttpRequest) -> JsonResponse:
    """
    Creates a User given the parameters provided in the HTTP Request
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if (not username and not email) or not password:
        return JsonResponse(
            {"details": "Must provide valid Username/Email and Password"}, status=406
        )

    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")

    User = get_user_model()
    if (
        User.objects.filter(username=username).exists()
        or User.objects.filter(email=email).exists()
    ):
        return JsonResponse({"details": "Username/Email Already Exists!"}, status=409)

    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

    if user is not None:
        login(request, user)
        return JsonResponse({"details": "User Created and Logged in"}, status=201)
    return JsonResponse({"details": "Authentication Failed"}, status=500)


@require_http_methods(["POST"])
def loginUser(request: HttpRequest) -> JsonResponse:
    """
    Attempts to login a User with Username/Email and a Password
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if (username is None and email is None) or password is None:
        return JsonResponse(
            {"details": "Must Provide Username/Email and Password"}, status=406
        )

    if username is None:
        user = User.objects.filter(email=email).first()

        if user is None:
            return JsonResponse({"details": "Invalid Username/Email and/or Password"}, status=404
        )

        username = user.username

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse(
            {"details": "Invalid Username/Email and/or Password"}, status=404
        )

    login(request, user)
    return JsonResponse({"details": "User logged in"}, status=200)


@require_http_methods(["POST"])
def logoutUser(request: HttpRequest) -> JsonResponse:
    """
    Logs out the authenticated user
    """
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"details": "User Logged Out"}, status=200)
    return JsonResponse({"details": "No User is Currently Logged In"}, status=400)


@require_http_methods(["PUT"])
def updateUser(request: HttpRequest) -> JsonResponse:
    """
    Updates an attribute of the authenticated User
    """
    if not request.user.is_authenticated:
        return JsonResponse({"details": "No User is Currently Logged In"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    attr = data.get("attribute")
    new_val = data.get("new_value")

    if not attr or new_val is None:
        return JsonResponse({"details": "Attribute or new value missing"}, status=406)

    allowed_attrs = ["first_name", "last_name", "email", "user_type"]
    if attr not in allowed_attrs:
        return JsonResponse({"details": "Invalid Attribute"}, status=406)

    if attr == "user_type" and new_val not in ["user", "organization", "driver"]:
        return JsonResponse({"details": "Invalid user type"}, status=406)

    setattr(request.user, attr, new_val)
    request.user.save()
    return JsonResponse({"details": "Attribute Updated"}, status=200)


@require_http_methods(["GET"])
def getUserInfo(request: HttpRequest) -> JsonResponse:
    """
    Returns basic details of the authenticated User
    """
    if request.user.is_authenticated:
        user = request.user
        info = {
            "username": user.get_username(),
            "email": user.get_email(),
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "user_type": user.get_role(),
        }
        return JsonResponse(info, status=200)

    return JsonResponse({"details": "No User is Currently Logged In"}, status=400)
