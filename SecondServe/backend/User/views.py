"""
Manages User Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


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

    if (username is None and email is None) or password is None:
        return JsonResponse(
            {"details": "Must provide valid Username/Email and Password" & password }, status=406
        )

    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")

    User = get_user_model()
    if (
        User.objects.filter(username=username).exists()
        or User.objects.filter(email=email).exists()
    ):
        return JsonResponse({"details": "Username/Email Already Exists!"}, status=409)

    user = User(
        username=username, email=email, first_name=first_name, last_name=last_name
    )
    user.set_password(password)  # hash the password
    user.save()

    if username is None:
        username = email

    authuser = authenticate(username=username, password=password)
    if authuser is not None:
        login(request, authuser)
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
        username = email

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
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_type": user.user_type,
        }
        return JsonResponse(info, status=200)

    return JsonResponse({"details": "No User is Currently Logged In"}, status=400)
