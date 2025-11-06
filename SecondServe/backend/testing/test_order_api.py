from django.contrib.auth import get_user_model
from django.test import TestCase
from Organization.models import Organization, TYPE_GROCERYSTORE
from Inventory.models import Item
from Order.models import Order, OrderedItem
import json

User = get_user_model()

class BaseOrderTestCase(TestCase):
    """
    Sets up a common baseline for test cases evaluating Order functionality
    """

    @classmethod
    def setUpTestCase(self):
        """
        Creates four User Accounts, an Organization, and Three Items for the Organization Inventory
        User Accounts:
        * userA: userA/alpha, userA@gmail.com, user
        * userB: userB/bravo, userB@gmail.com, user
        * user_driver: driver/driving, driving@gmail.com, driver
        * user_org: orgUser/orgo, bigOrg@gmail.com, organization
        * user_notOrg: notOrg/orgoNoNo, notOrg@gmail.com, organization
        """



        # Create User Account 1
        self.user_a = User.objects.create_user(
            username="userA", email="userA@gmail.com", password="alpha", role="user"
        )

        # Create User Account 2
        self.user_b = User.objects.create_user(
            username="userB", email="userB@gmail.com", password="bravo", role="user"
        )

        # Create Driver Account
        self.user_driver = User.objects.create_user(
            username="driver", email="driving@gmail.com", password="driving", role="driver"
        )

        # Create Organization User Account
        self.user_org = User.objects.create_user(
            username="orgUser", email="bigOrg@gmail.com", password="orgo", role="organization"
        )

        # Create Organization User Account (not creator of org)
        self.user_org_not = User.objects.create_user(
            username="notOrg", email="notOrg@gmail.com", password="orgoNoNo", role="organization"
        )

        # Create Organization
        self.org = Organization.objects.create(
            name="BigOrg",
            orgType=TYPE_GROCERYSTORE,
            location="123 Highway NC",
            user=self.user_org
        )

        # Create Items for Organization Inventory
        orgInv = self.org.inv
        
        # Pasta, Shelf Stable, 10, Expires 12-01-25
        self.itemP = Item.objects.create(
            name="Pasta",
            type= Item.ItemType.STABLE,
            quantity = 10,
            expiration="December 1, 2025",
            inventoyr=orgInv
        ).to_dict()

        # Lettuce, Produce, 25, Expires 11-15-25
        self.itemL = Item.objects.create(
            name="Lettuce",
            type= Item.ItemType.PRODUCE,
            quantity = 25,
            expiration="December 1, 2025",
            inventoyr=orgInv
        ).to_dict()

        # Milk, Refrigderated, 5, Expires 11-30-25
        self.itemM = Item.objects.create(
            name="Milk",
            type= Item.ItemType.REFRIG,
            quantity = 5,
            expiration="November 30, 2025",
            inventoyr=orgInv
        ).to_dict()

class testNoLoggedInUser(TestCase):
    """
    Tests Order API functionality with no logged in User
    """

    def test_get_available_items(self):
        response = self.client.get("/items/bigOrg/")
        self.assertEqual(response.status_code, 400)

    def test_place_order(self):
        response = self.client.post("/order/place/")
        self.assertEqual(response.status_code, 400)

    def test_get_active_orders(self):
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 400)

    def test_get_open_orders(self):
        response = self.client.get("/orders/open/")
        self.assertEqual(response.status_code, 400)

    def test_update_order(self):
        response = self.client.put("/order/0/update/")
        self.assertEqual(response.status_code, 400)

    def test_single_order_action(self):
        response = self.client.get("/order/0/")
        self.assertEqual(response.status_code, 400)

class testInvalidUserRole(BaseOrderTestCase):
    def test_invalid_place_order(self):
        pass
    
    def test_invalid_get_available_items(self):
        # Driver
        self.client.force_login(self.user_driver)
        response = self.client.get("/items/bigOrg/")
        self.assertEqual(response.status_code, 403)

        # Org but not creator
        self.client.force_login(self.user_org_not)
        response = self.client.get("/items/bigOrg/")
        self.assertEqual(response.status_code, 401)

    def test_invalid_place_order(self):
        # Driver
        self.client.force_login(self.user_driver)
        response = self.client.post("/order/place/")
        self.assertEqual(response.status_code, 403)

        # Org but not creator
        self.client.force_login(self.user_org)
        response = self.client.post("/order/place/")
        self.assertEqual(response.status_code, 403)

    def test_invalid_get_open_orders(self):
        # User Account
        self.client.force_login(self.user_a)
        response = self.client.get("/orders/open/")
        self.assertEqual(response.status_code, 403)

class testGetAvailableItems(BaseOrderTestCase):

    def test_invalid_org(self):

        self.client.force_login(self.user_a)

        response = self.client.get("/items/fakeOrg/")
        self.assertEqual(response.status_code, 404)


    def test_valid_get(self):

        self.client.force_login(self.user_a)

        response = self.client.get("/items/bigOrg/")
        self.assertEqual(response.status_code, 200)

        responseItems = response.get("items")

        for item in responseItems:
            match item["name"]:
                case "milk":
                    self.assertEqual(item["type"], self.itemM["type"])
                    self.assertEqual(item["quantity"], self.itemM["quantity"])
                    self.assertEqual(item["expiration"], self.itemM["expiration"])
                case "lettuce":
                    self.assertEqual(item["type"], self.itemL["type"])
                    self.assertEqual(item["quantity"], self.itemL["quantity"])
                    self.assertEqual(item["expiration"], self.itemL.expiration)
                case "pasta":
                    self.assertEqual(item["type"], self.itemP["type"])
                    self.assertEqual(item["quantity"], self.itemP["quantity"])
                    self.assertEqual(item["expiration"], self.itemP["expiration"])
                case _:
                    self.assertFalse(True)

class testPlaceOrder(BaseOrderTestCase):

    def test_invalid_order(self):

        # Org doesnt exist

        # Item doesn't exist

        # Invalid quantity
        pass

    def test_valid_order(self):

        # Single Item

        # Multi Item

        pass

class testGetActiveOrders(BaseOrderTestCase):

    def setUp(self):

        # User A Creates Order (1 Pasta, 2 Lettuce)
        self.orderA = Order.objects.create(
            recipient=self.user_a,
            associatedOrg=self.org
        )
        
        

        # User-2 Creates Order
            # 2 Milk, 3 Lettuce

        # Driver Claims User-2 Order

        return super().setUp()

    def test_valid_user(self):
        # User A only sees their order


        # User B only sees their order

        pass

    def test_valid_org(self):

        # Org sees both Orders

        pass

    def test_valid_driver(self):

        # Driver only sees their claimed order

        pass

class testGetOpenOrders(BaseOrderTestCase):

    def setUp(self):

        # User-1 Creates Order
            # 1 Pasta, 2 Lettuce

        # User-2 Creates Order
            # 2 Milk, 3 Lettuce

        return super().setUp()

    def test_invalid_user(self):
        # User role

        pass

    def test_valid_org(self):

        pass

    def test_valid_driver(self):

        pass


class testUpdateOrder(TestCase):

    def setUp(self):
        return super().setUp()

    def test_invalid_user(self):
        # User role

        pass

    def test_invalid_status(self):

        # Driver passes org status

        # Org passes Driver status

        # Driver passes invalid status
        
        pass

    def test_valid_org(self):

        pass

    def test_valid_driver(self):

        pass

class testGetOrder(TestCase):
    def setUp(self):
        return super().setUp()

    def test_invalid_user(self):
        # Not logged in

        # User role

        pass

    def test_invalid_status(self):

        # Driver passes org status

        # Org passes Driver status

        # Driver passes invalid status
        
        pass

    def test_valid_org(self):

        pass

    def test_valid_driver(self):

        pass

class testClaimOrder(TestCase):
    def setUp(self):
        return super().setUp()
    
    def test_invalid_user(self):
        # Not logged in
        response = self.client.put("/order/0/")
        self.assertEqual(response.status_code, 400)

        # User role

        # Org role

        pass

    def test_invalid_claim(self):
        # Attempt to claim non-extisent order

        # Attempt to claim order already claimed
        
        pass

    def test_valid_claim(self):
        pass