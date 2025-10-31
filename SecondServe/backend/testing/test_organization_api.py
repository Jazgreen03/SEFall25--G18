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


class TestValidUserCreateOrganization(TestCase):

    # Creates a user with the location permission for testing purposes and logins them into the system
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


    # Create a valid Organization and verify the response
    def test_valid_org_create(self):
        response = self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

        self.assertEqual(response.status_code, 201)

    # Attempt to create Invalid Organization and verify the response
    def test_invalid_org_create(self):
        
        # Create the base case valid organization
        self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )


        # Invalid Type
        response = self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": invalid_orgType,
                "location": orgLocation
            }
        )

        self.assertEqual(response.status_code, 404)

        # Invalid Name
        response = self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocationTwo
            }
        )

        self.assertEqual(response.status_code, 409)

        # Invalid Location
        response = self.client.post(
            "org/", 
            {
                "name": orgNameTwo,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

        self.assertEqual(response.status_code, 409)


# Attempt to create Organization with user account with invalid credentials
class TestInvalidUserCreateOrganization(TestCase):

    def test_no_logged_in_user(self):
        response = self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_role(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "user"
        self.user.save()

        self.client.post(
            "/user/login/",
            {
                "email": "org@email.com",
                "password": "123abc"
            }
        )

        response = self.client.post(
            "org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

        self.assertEqual(response.status_code, 401)
