from django.contrib.auth import get_user_model
from django.test import TestCase
import json

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
            username="orgUser", email="org@email.com", password="123abc"
        )
        self.user.role = "organization"
        self.user.save()

        # Log user in
        self.client.force_login(self.user)

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
            username="orgUser", email="org@email.com", password="123abc"
        )
        self.user.role = "user"
        self.user.save()

        # Log user in
        self.client.force_login(self.user)

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
            username="orgUser", email="org@email.com", password="123abc"
        )
        self.user.role = "organization"
        self.user.save()

        self.client.force_login(self.user)

        self.client.post(
            "/org/", data=json.dumps({"name": orgName, "type": valid_orgType, "location": orgLocation}),
            content_type="application/json",
        )

    def test_valid_item_add(self):
        # Add the item
        response = self.client.post(
            "/inventory/add/", data=json.dumps(
            {
                "item_name": "pasta",
                "quantity": "30",
                "expiration": "December 31, 2030",
                "type": "stable",
            }),
            content_type="application/json",
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
            "/inventory/add/", data=json.dumps(
            {
                "item_name": "milk",
                "quantity": "5",
                "expiration": "November 30, 2025",
                "type": "refrigerated",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # Get the inventory and verify the item was added
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        inventory = data["inventory"]
        self.assertEqual(len(inventory), 2)

        # Verify the item details are correct
        if inventory[1]["name"] == "milk":
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
            username="orgUser", email="org@email.com", password="123abc"
        )
        self.user.role = "organization"
        self.user.save()

        self.client.force_login(self.user)

        self.client.post(
            "/org/", data=json.dumps({"name": orgName, "type": valid_orgType, "location": orgLocation}),
            content_type="application/json",
        )

        # Item 1
        self.client.post(
            "/inventory/add/", data=json.dumps(
            {
                "item_name": "pasta",
                "quantity": "30",
                "expiration": "December 31, 2030",
                "type": "stable",
            }),
            content_type="application/json",
        )

        # Item 2
        self.client.post(
            "/inventory/add/", data=json.dumps(
            {
                "item_name": "milk",
                "quantity": "5",
                "expiration": "November 30, 2025",
                "type": "refrigerated",
            }),
            content_type="application/json",
        )

        # Item 3
        self.client.post(
            "/inventory/add/", data=json.dumps(
            {
                "item_name": "lettuce",
                "quantity": "15",
                "expiration": "November 15, 2025",
                "type": "produce",
            }),
            content_type="application/json",
        )

        # Item 4
        self.client.post(
            "/inventory/add/", data=json.dumps(
            {
                "item_name": "pizza",
                "quantity": "1",
                "expiration": "November 5, 2025",
                "type": "prepared",
            }),
            content_type="application/json",
        )

    def test_valid_single_attr_update(self):

        item1Update = {
            "item_name": "pasta",
            "attributes": ["quantity"],
            "values": ["50"],
        }
        item2Update = {
            "item_name": "milk",
            "attributes": ["expiration"],
            "values": ["November 20, 2025"],
        }
        item4Update = {
            "item_name": "pizza",
            "attributes": ["type"],
            "values": ["refrigerated"],
        }

        response = self.client.put(
            "/inventory/update/",
            data=json.dumps({"items": [item1Update, item2Update, item4Update]}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        # Verify the items were changed
        response = self.client.get("/inventory/")
        data = response.json()
        inventory = data["inventory"]

        for item in inventory:
            match item["name"]:
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

    def test_valid_multi_attr_val_update(self):
        item1Update = {
            "item_name": "pasta",
            "attributes": ["name", "quantity"],
            "values": ["macaroni", "50"],
        }
        item4Update = {
            "item_name": "pizza",
            "attributes": ["type", "expiration"],
            "values": ["refrigerated", "November 21, 2025"],
        }

        response = self.client.put(
            "/inventory/update/",
            data=json.dumps({"items": [item1Update, item4Update]}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        # Verify the items were changed
        response = self.client.get("/inventory/")
        data = response.json()
        inventory = data["inventory"]

        for item in inventory:
            match item["name"]:
                # Only the quantity should have changed
                case "macaroni":
                    self.assertEqual(item["quantity"], 50)
                    self.assertEqual(item["expiration"], "December 31, 2030")
                    self.assertEqual(item["type"], "Shelf Stable")

                # Only the expiration date should have changed
                case "milk":
                    self.assertEqual(item["quantity"], 5)
                    self.assertEqual(item["expiration"], "November 30, 2025")
                    self.assertEqual(item["type"], "Refrigerated")

                # Lettuce should remain untouched
                case "lettuce":
                    self.assertEqual(item["quantity"], 15)
                    self.assertEqual(item["expiration"], "November 15, 2025")
                    self.assertEqual(item["type"], "Produce")

                # Only the type should have changed
                case "pizza":
                    self.assertEqual(item["quantity"], 1)
                    self.assertEqual(item["expiration"], "November 21, 2025")
                    self.assertEqual(item["type"], "Refrigerated")

                # If an invalid item name is passed for the test case
                case _:
                    self.fail("Invalid Item in Inventory")

    def test_invalid_update(self):

        # Differing lengths between attributes and values
        itemUpdate = {
            "item_name": "pasta",
            "attributes": ["name", "quantity"],
            "values": ["macaroni"],
        }
        response = self.client.put(
            "/inventory/update/",
            data=json.dumps({"items": [itemUpdate]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

        # No Item Name
        itemUpdate = {"attributes": ["name"], "values": ["macaroni"]}
        response = self.client.put(
            "/inventory/update/",
            data=json.dumps({"items": [itemUpdate]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

        # Nonexistent Item Name
        itemUpdate = {
            "item_name": "Curly Fries",
            "attributes": ["name", "quantity"],
            "values": ["macaroni", "50"],
        }
        response = self.client.put(
            "/inventory/update/",
            data=json.dumps({"items": [itemUpdate]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)


class TestEditItem(TestCase):

    # Creates a user, organization, and an item for the inventory
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser", email="org@email.com", password="123abc"
        )
        self.user.role = "organization"
        self.user.save()

        self.client.force_login(self.user)

        self.client.post(
            "/org/", data=json.dumps({"name": orgName, "type": valid_orgType, "location": orgLocation}),
            content_type="application/json",
        )

        # Item
        self.client.post(
            "/inventory/add/",data=json.dumps(
            {
                "item_name": "pasta",
                "quantity": 30,
                "expiration": "December 31, 2030",
                "type": "stable",
            }),
            content_type="application/json",
        )

    def test_valid_single_attr_edit(self):

        itemUpdate = {"item_name": "pasta", "attributes": ["quantity"], "values": [50]}

        response = self.client.put(
            "/inventory/edit/",
            data=json.dumps(itemUpdate),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Verify the items were changed
        response = self.client.get("/inventory/")
        data = response.json()
        inventory = data["inventory"]
        item = inventory[0]

        self.assertEqual(item["name"], "pasta")
        self.assertEqual(item["quantity"], 50)
        self.assertEqual(item["expiration"], "December 31, 2030")
        self.assertEqual(item["type"], "Shelf Stable")

    def test_valid_multi_attr_val_edit(self):
        itemUpdate = {
            "item_name": "pasta",
            "attributes": ["name", "quantity"],
            "values": ["macaroni", 50],
        }

        response = self.client.put(
            "/inventory/edit/",
            data=json.dumps(itemUpdate),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        # Verify the items were changed
        response = self.client.get("/inventory/")
        data = response.json()
        inventory = data["inventory"]

        item = next(i for i in inventory if i["name"] == "macaroni")

        self.assertEqual(item["name"], "macaroni")
        self.assertEqual(item["quantity"], 50)
        self.assertEqual(item["expiration"], "December 31, 2030")
        self.assertEqual(item["type"], "Shelf Stable")

    def test_invalid_edit(self):

        # Differing lengths between attributes and values
        itemUpdate = {
            "item_name": "pasta",
            "attributes": ["name", "quantity"],
            "values": ["macaroni"],
        }
        response = self.client.put(
            "/inventory/edit/",
            data=json.dumps(itemUpdate),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

        # No Item Name
        itemUpdate = {"attributes": ["name"], "values": ["macaroni"]}
        response = self.client.put(
            "/inventory/edit/",
            data=json.dumps(itemUpdate),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

        # Nonexistent Item Name
        itemUpdate = {
            "item_name": "Curly Fries",
            "attributes": ["name", "quantity"],
            "values": ["macaroni", "50"],
        }
        response = self.client.put(
            "/inventory/edit/",
            data=json.dumps(itemUpdate),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
