from django.contrib.auth import get_user_model
from django.test import TestCase
from Organization.models import Organization, TYPE_GROCERYSTORE
from Inventory.models import Item
from Order.models import Order, OrderedItem
import json
from datetime import datetime

User = get_user_model()

class BaseOrderTestCase(TestCase):
    """
    Sets up a common baseline for test cases evaluating Order functionality
    """

    def setUp(cls):
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
        cls.user_a = User.objects.create_user(
            username="alphaUser", email="alphaUser@gmail.com", password="alpha", role="user"
        )

        # Create User Account 2
        cls.user_b = User.objects.create_user(
            username="bravoUser", email="bravoUser@gmail.com", password="bravo", role="user"
        )

        # Create Driver Account
        cls.user_driver = User.objects.create_user(
            username="driver", email="driving@gmail.com", password="driving", role="driver"
        )

        # Create Organization User Account
        cls.user_org = User.objects.create_user(
            username="bigOrgPeep", email="bigOrg@gmail.com", password="orgo", role="organization"
        )

        # Create Organization User Account (not creator of org)
        cls.user_org_not = User.objects.create_user(
            username="notOrgPeep", email="notOrg@gmail.com", password="orgoNoNo", role="organization"
        )

        # Create Organization
        cls.org = Organization.objects.createOrganization(
            name="BigOrg",
            orgType=TYPE_GROCERYSTORE,
            location="123 Highway NC",
            user=cls.user_org
        )

        # Create Items for Organization Inventory
        orgInv = cls.org.inv
        
        # Pasta, Shelf Stable, 10, Expires 12-01-25
        cls.itemPItem = Item.objects.create(
            name="Pasta",
            type= Item.ItemType.STABLE,
            quantity = 10,
            expiration=datetime.strptime("December 1, 2025", "%B %d, %Y").date(),
            inventory=orgInv
        )
        cls.itemP = cls.itemPItem.to_dict()

        # Lettuce, Produce, 25, Expires 11-15-25
        cls.itemLItem = Item.objects.create(
            name="Lettuce",
            type= Item.ItemType.PRODUCE,
            quantity = 25,
            expiration=datetime.strptime("November 15, 2025", "%B %d, %Y").date(),
            inventory=orgInv
        )
        cls.itemL = cls.itemLItem.to_dict()

        # Milk, Refrigderated, 5, Expires 11-30-25
        cls.itemMItem = Item.objects.create(
            name="Milk",
            type= Item.ItemType.REFRIG,
            quantity = 5,
            expiration=datetime.strptime("November 30, 2025", "%B %d, %Y").date(),
            inventory=orgInv
        )
        cls.itemM = cls.itemMItem.to_dict()

        cls.orderListA = [{"name": "Pasta", "quantity": 1}, {"name": "Lettuce", "quantity": 2}]
        cls.orderListB = [{"name":"Milk", "quantity":2}, {"name": "Lettuce", "quantity":3}]
        cls.fakeOrder = [{"name":"wine", "quantity":1}, {"name": "cash", "quantity":700}]

class TestNoLoggedInUser(TestCase):
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

class TestInvalidUserRole(BaseOrderTestCase):
    """
    Test Order API Functionality where API Calls are provided User's with
    invalid Roles for the specified API call
    """

    def setUp(self):
        super().setUp()

    def test_invalid_place_order(self):
        # Driver
        self.client.force_login(self.user_driver)
        response = self.client.post("/order/place/")
        self.assertEqual(response.status_code, 403)

        # Organization
        self.client.force_login(self.user_org)
        response = self.client.post("/order/place/")
        self.assertEqual(response.status_code, 403)
    
    def test_invalid_get_available_items(self):
        # Driver
        self.client.force_login(self.user_driver)
        response = self.client.get("/items/BigOrg/")
        self.assertEqual(response.status_code, 403)

        # Org but not creator
        self.client.force_login(self.user_org_not)
        response = self.client.get("/items/BigOrg/")
        self.assertEqual(response.status_code, 401)

    def test_invalid_get_open_orders(self):
        # User Account
        self.client.force_login(self.user_a)
        response = self.client.get("/orders/open/")
        self.assertEqual(response.status_code, 403)

class testGetAvailableItems(BaseOrderTestCase):
    """
    Tests the specific functionality found in the getAvailableItems API Call
    """
    def setUp(self):
        super().setUp()
    
    def test_invalid_org(self):

        self.client.force_login(self.user_a)

        response = self.client.get("/items/fakeOrg/")
        self.assertEqual(response.status_code, 404)


    def test_valid_get(self):

        self.client.force_login(self.user_a)

        response = self.client.get("/items/BigOrg/")
        self.assertEqual(response.status_code, 200)

        responseItems = response.get("items", [])

        for item in responseItems:
            match item.get("name"):
                case "milk":
                    self.assertEqual(item.get("type"), self.itemM.get("type"))
                    self.assertEqual(item.get("quantity"), self.itemM.get("quantity"))
                    self.assertEqual(item.get("expiration"), self.itemM.get("expiration"))
                case "lettuce":
                    self.assertEqual(item.get("type"), self.itemL.get("type"))
                    self.assertEqual(item.get("quantity"), self.itemL.get("quantity"))
                    self.assertEqual(item.get("expiration"), self.itemL.get("expiration"))
                case "pasta":
                    self.assertEqual(item.get("type"), self.itemP.get("type"))
                    self.assertEqual(item.get("quantity"), self.itemP.get("quantity"))
                    self.assertEqual(item.get("expiration"), self.itemP.get("expiration"))
                case _:
                    self.assertFalse(True)

class testPlaceOrder(BaseOrderTestCase):

    def setUp(self):
        super().setUp()
    
    def test_invalid_order(self):

        self.client.force_login(self.user_a)

        # Org doesnt exist
        response = self.client.post("/order/place/", data=json.dumps({"organization_name": "fakeOrg"}), content_type="application/json")

        # Item doesn't exist
        response = self.client.post("/order/place/", data=json.dumps({"organization_name": "BigOrg", "items": self.fakeOrder}), content_type="application/json")

        # Invalid quantity
        response = self.client.post("/order/place/", data=json.dumps({"organization_name": "BigOrg", "items": [{"name": "Pasta", "quantity": 100}]}), content_type="application/json")
        self.assertEqual(response.status_code, 404)

        pass

    def test_valid_order(self):

        self.client.force_login(self.user_a)

        # Single Item
        response = self.client.post("/order/place/", data=json.dumps({"organization_name": "BigOrg", "items": [{"name": "Pasta", "quantity": 1}]}), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        self.client.force_login(self.user_b)

        # Multi Item
        response = self.client.post("/order/place/", data=json.dumps({"organization_name": "BigOrg", "items": self.orderListA}), content_type="application/json")
        self.assertEqual(response.status_code, 201)

class UpgradedOrderTestCase(BaseOrderTestCase):

    def setUp(cls):
        super().setUp()

        # User A Creates Order (1 Pasta, 2 Lettuce)
        cls.orderA = Order.objects.create(
            recipient=cls.user_a,
            associatedOrg=cls.org,
            status = Order.StatusTypes.READY
        )

        cls.orderAI_A = OrderedItem.objects.create(
            associatedItem=cls.itemPItem,
            associatedOrder=cls.orderA,
            numOfItem=1
        )

        cls.orderAI_B = OrderedItem.objects.create(
            associatedItem=cls.itemLItem,
            associatedOrder=cls.orderA,
            numOfItem=2
        )
        
        # User-2 Creates Order (2 Milk, 3 Lettuce)
        # With Driver 2 having "claimed" it
        cls.orderB = Order.objects.create(
            recipient=cls.user_b,
            associatedOrg=cls.org,
            driver=cls.user_driver,
            driverAssigned=True,
            status = Order.StatusTypes.PREPARING
        )

        cls.orderBI_A = OrderedItem.objects.create(
            associatedItem=cls.itemMItem,
            associatedOrder=cls.orderB,
            numOfItem=2
        )

        cls.orderBI_B = OrderedItem.objects.create(
            associatedItem=cls.itemLItem,
            associatedOrder=cls.orderB,
            numOfItem=3
        )
class testGetActiveOrders(UpgradedOrderTestCase):

    def setUp(self):
        
        super().setUp()

    def test_valid_user(self):
        # User A only sees their order
        self.client.force_login(self.user_a)
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        orders = response.json().get("Active Orders", [])
        order = orders[0]

        self.assertEqual(order.get("Order ID"), self.orderA.orderID)


        # User B only sees their order
        self.client.force_login(self.user_b)
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        orders = response.json().get("Active Orders", [])
        order = orders[0]

        self.assertEqual(order.get("Order ID"), self.orderB.orderID)

        pass

    def test_valid_org(self):

        # Org sees both Orders
        self.client.force_login(self.user_org)
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)

        orders = response.json().get("Active Orders", [])

        self.assertEqual(len(orders), 2)

    def test_valid_driver(self):

        # Driver only sees their claimed order
        self.client.force_login(self.user_driver)
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)

        orders = response.json().get("Active Orders", [])
        order = orders[0]

        self.assertEqual(order.get("Order ID"), self.orderB.orderID)

        pass

class testGetOpenOrders(UpgradedOrderTestCase):

    def setUp(self):
        super().setUp()

    def test_valid_org(self):
        self.client.force_login(self.user_org)
        response = self.client.get("/orders/open/")
        self.assertEqual(response.status_code, 200)

        # Check there are two orders
        orders = response.json().get("Orders", [])

        self.assertEqual(len(orders), 2)


    def test_valid_driver(self):
        self.client.force_login(self.user_driver)
        response = self.client.get("/orders/open/")
        self.assertEqual(response.status_code, 200)

        # Check the order pulled matches the right OrderID
        orders = response.json().get("Orders", [])
        self.assertEqual(len(orders), 1)
        order = orders[0]

        self.assertEqual(order.get("Order ID"), self.orderA.orderID)

class testGetOrder(UpgradedOrderTestCase):
    
    def setUp(self):
        
        super().setUp()

    def test_invalid_get_order(self):
        self.client.force_login(self.user_driver)

        # Invalid ID
        response = self.client.get("/order/0/")
        self.assertEqual(response.status_code, 404)

    def test_valid_get_order(self):

        self.client.force_login(self.user_a)

        response = self.client.get(f"/order/{self.orderA.orderID}/")
        self.assertEqual(response.status_code, 200)

class testClaimOrder(UpgradedOrderTestCase):
    
    def setUp(self):
        
        super().setUp()

    def test_invalid_claim(self):
        self.client.force_login(self.user_driver)

        # Attempt to claim non-extisent order
        response = self.client.put("/order/0/")
        self.assertEqual(response.status_code, 404)

        # Attempt to claim order already claimed
        response = self.client.put(f"/order/{self.orderB.orderID}/")
        self.assertEqual(response.status_code, 403)


    def test_valid_claim(self):
        self.client.force_login(self.user_driver)

        response = self.client.put(f"/order/{self.orderA.orderID}/")
        self.assertEqual(response.status_code, 200)