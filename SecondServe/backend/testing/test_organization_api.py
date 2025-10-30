import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from Inventory.models import Inventory, Item
from Organization.models import Organization

User = get_user_model()

orgName = "Organization"
orgNameTwo = "Org"

valid_orgType = "foodbank"
invalid_orgType = "hospital"

orgLocation = "NC State University"
orgLocationTwo = "UNC Chapel Hill"


class TestCreateOrganization(TestCase):

    # Creates a user with the location permission for testing purposes
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

    # Create a valid Organization and verify the response

    # Attempt to create Invalid Organization and verify the response

    # Attempt to create Organization with user account with invalid credentials

    

