"""
Manages User Functionality, called by urls.py
"""

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["POST"])
def createUser(request: HttpRequest) -> JsonResponse:
    """
    Creates a User given the parameters provided in the HTTP Request
    """
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    if not username or not password or not email:
        return JsonResponse(
            {"details": "Must provide valid Username, Password, and Email"}, status=406
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
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    if (not username and not email) or not password:
        return JsonResponse(
            {"details": "Must Provide Username/Email and Password"}, status=406
        )

    User = get_user_model()
    if email and not username:
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            return JsonResponse({"details": "Invalid credentials"}, status=404)

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

    # Parse JSON body for PUT requests
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON"}, status=400)

    attr = data.get("attribute")
    new_val = data.get("new_value")

    if not attr or new_val is None:
        return JsonResponse({"details": "Attribute or new value missing"}, status=406)

    allowed_attrs = ["first_name", "last_name", "email", "username"]
    if attr not in allowed_attrs:
        return JsonResponse({"details": "Invalid Attribute"}, status=406)

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
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return JsonResponse(info, status=200)

    return JsonResponse({"details": "No User is Currently Logged In"}, status=400)
