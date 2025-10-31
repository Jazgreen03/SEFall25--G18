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

        self.client.force_login(self.user)

        self.client.post(
            "/org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

    def test_valid_item_add(self):
        # Add the item
        response = self.client.post(
            "/inventory/add/",
            {
                "item_name": "pasta",
                "quantity": "30",
                "expiration": "December 31, 2030",
                "type": "stable"
            }
        )

        self.assertEqual(response.status_code, 201)

        # Get the inventory and verify the item was added
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        inventory = data["inventory"]
        self.assertEqual(len(inventory), 1)

        # Verify the item details are correct
        item = inventory[0]
        self.assertEqual(item["name"], "pasta")
        self.assertEqual(item["type"], "Shelf Stable")
        self.assertEqual(item["quantity"], 30)
        self.assertEqual(item["expiration"], "December 31, 2030")

        # Add a second item
        response = self.client.post(
            "/inventory/add/",
            {
                "item_name": "milk",
                "quantity": "5",
                "expiration": "November 30, 2025",
                "type": "refrigerated"
            }
        )
        self.assertEqual(response.status_code, 201)

        # Get the inventory and verify the item was added
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        inventory = data["inventory"]
        self.assertEqual(len(inventory), 2)

        # Verify the item details are correct
        if (inventory[1]["name"] is "milk"):
            item = inventory[1]
        else:
            item = inventory[0]
        self.assertEqual(item["name"], "milk")
        self.assertEqual(item["type"], "Refrigerated")
        self.assertEqual(item["quantity"], 5)
        self.assertEqual(item["expiration"], "November 30, 2025")


class TestUpdateInventory(TestCase):

    # Creates a user, organization, and items for an inventory
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        self.client.force_login(self.user)

        self.client.post(
            "/org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

        # Item 1
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "pasta",
                "quantity": "30",
                "expiration": "December 31, 2030",
                "type": "stable"
            }
        )

        # Item 2
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "milk",
                "quantity": "5",
                "expiration": "November 30, 2025",
                "type": "refrigerated"
            }
        )

        # Item 3
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "lettuce",
                "quantity": "15",
                "expiration": "November 15, 2025",
                "type": "produce"
            }
        )
        
        # Item 4
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "pizza",
                "quantity": "1",
                "expiration": "November 5, 2025",
                "type": "prepared"
            }
        )
    
    def test_valid_single_attr_update(self):
        
        item1Update = {"item_name": "pasta", "attributes": ["quantity"], "values": ["50"]}
        item2Update = {"item_name": "milk", "attributes": ["expiration"], "values": ["November 20, 2025"]}
        item4Update = {"item_name": "pizza", "attributes": ["type"], "values": ["refrigerated"]}
        
        response = self.client.put(
            "/inventory/update/", 
            {
                "items": [item1Update, item2Update, item4Update]
            }
        )

        self.assertEqual(response.status_code, 200)

        # Verify the items were changed
        response = self.client.get("/inventory/")
        data = response.json()
        inventory = data["inventory"]

        for item in inventory:
            match item["item_name"]:
                # Only the quantity should have changed
                case "pasta":
                    self.assertEqual(item["quantity"], 50)
                    self.assertEqual(item["expiration"], "December 31, 2030")
                    self.assertEqual(item["type"], "Shelf Stable")

                # Only the expiration date should have changed
                case "milk":
                    self.assertEqual(item["quantity"], 5)
                    self.assertEqual(item["expiration"], "November 20, 2025")
                    self.assertEqual(item["type"], "Refrigerated")

                # Lettuce should remain untouched
                case "lettuce":
                    self.assertEqual(item["quantity"], 15)
                    self.assertEqual(item["expiration"], "November 15, 2025")
                    self.assertEqual(item["type"], "Produce")

                # Only the type should have changed
                case "pizza":
                    self.assertEqual(item["quantity"], 1)
                    self.assertEqual(item["expiration"], "November 5, 2025")
                    self.assertEqual(item["type"], "Refrigerated")
                
                # If an invalid item name is passed for the test case
                case _:
                    self.fail("Invalid Item in Inventory")





class TestEditItem(TestCase):

    # Creates a user, organization, and items for an inventory
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

        self.client.force_login(self.user)

        self.client.post(
            "/org/", 
            {
                "name": orgName,
                "type": valid_orgType,
                "location": orgLocation
            }
        )

        # Item 1
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "pasta",
                "quantity": "30",
                "expiration": "December 31, 2030",
                "type": "stable"
            }
        )

        # Item 2
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "milk",
                "quantity": "5",
                "expiration": "November 30, 2025",
                "type": "refrigerated"
            }
        )

        # Item 3
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "lettuce",
                "quantity": "15",
                "expiration": "November 15, 2025",
                "type": "produce"
            }
        )
        
        # Item 4
        self.client.post(
            "/inventory/add/",
            {
                "item_name": "pizza",
                "quantity": "1",
                "expiration": "November 5, 2025",
                "type": "prepared"
            }
        )
