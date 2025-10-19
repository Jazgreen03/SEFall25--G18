from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    # Roles for the user are limited to the following:
        # -> user
        # -> driver
        # -> supplier
        # -> admin
    role = models.CharField(max_length=10, default="user")

    # Login information is restricted to email (or username) and password
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField()

    # For reference/debugging
    creationDate = models.DateTimeField()

    pass