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


class TestInvalidUser(TestCase):

    # Creates a user with the location permission but is unassociated with an organization
    def test_no_associated_org(self):
        # Create user
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        # Log user in
        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        # Try to get an inventory
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 404)

    # Try getting an inventory without a logged in user
    def test_no_logged_in_user(self):
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 400)

    # Creates a user with the user permission and tries to get an inventory
    def test_invalid_role(self):
        # Create user
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "user"
        self.user.save()

        # Log user in
        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        # Try to get an inventory
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 401)

class TestAddItem(TestCase):

    # Creates a user with the location permission for testing purposes
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

class TestUpdateInventory(TestCase):

    # Creates a user with the location permission for testing purposes
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

class TestEditItem(TestCase):

    # Creates a user with the location permission for testing purposes
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

class TestGetInventory(TestCase):
    
    # Creates a user with the location permission for testing purposes
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()
