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

        # Try to add an item
        response = self.client.post("/inventory/add/")
        self.assertEqual(response.status_code, 404)

        # Try to update the inventory
        response = self.client.put("/inventory/update/")
        self.assertEqual(response.status_code, 404)

        # Try to edit an item
        response = self.client.put("/inventory/edit/")
        self.assertEqual(response.status_code, 404)

    # No Logged in User
    def test_no_logged_in_user(self):
        # Try to get the inventory
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 400)

        # Try to add an item
        response = self.client.post("/inventory/add/")
        self.assertEqual(response.status_code, 400)

        # Try to update the inventory
        response = self.client.put("/inventory/update/")
        self.assertEqual(response.status_code, 400)

        # Try to edit an item
        response = self.client.put("/inventory/edit/")
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

        # Try to add an item
        response = self.client.post("/inventory/add/")
        self.assertEqual(response.status_code, 401)

        # Try to update the inventory
        response = self.client.put("/inventory/update/")
        self.assertEqual(response.status_code, 401)

        # Try to edit an item
        response = self.client.put("/inventory/edit/")
        self.assertEqual(response.status_code, 401)

class TestAddItem(TestCase):

    # Creates a user with the location permission for testing purposes
    # User is also associated with an organization
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )


class TestUpdateInventory(TestCase):

    # Creates a user with the location permission for testing purposes
    # User is also associated with an organization
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

class TestEditItem(TestCase):

    # Creates a user with the location permission for testing purposes
    # User is also associated with an organization
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

class TestGetInventory(TestCase):
    
    # Creates a user with the location permission for testing purposes
    # User is also associated with an organization
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )
