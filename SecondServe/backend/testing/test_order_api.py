from django.contrib.auth import get_user_model
from django.test import TestCase
from Organization.models import Organization, TYPE_GROCERYSTORE
import json

User = get_user_model()

class BaseOrderTestCase(TestCase):
    """
    Sets up a common baseline for test cases evaluating Order functionality
    """

    @classmethod
    def setUpTestCase(self):
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

        # Create Organization
        self.org = Organization.objects.create(
            name="BigOrg",
            orgType=TYPE_GROCERYSTORE,
            location="123 Highway NC",
            user=self.user_org
        )
        

        # Create Items for Inventory
            # Pasta, Shelf Stable, 10, Expires 12-01-25
            # Lettuce, Produce, 25, Expires 11-15-25
            # Milk, Refrigderated, 5, Expires 11-30-25
        
        pass


class testNoLoggedInUser(TestCase):

    def test_get_available_items(self):
        response = self.client.get("/items/basicOrg/")
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


class testGetAvailableItems(BaseOrderTestCase):

    def test_invalid_user(self):
        # Driver

        # Org but not creator

        pass


    def test_invalid_org(self):

        # Org doesnt exist

        pass


    def test_valid_get(self):

        pass

class testPlaceOrder(BaseOrderTestCase):


    def test_invalid_user(self):
        # Driver

        # Org
        pass

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

        # User-1 Creates Order
            # 1 Pasta, 2 Lettuce

        # User-2 Creates Order
            # 2 Milk, 3 Lettuce

        # Driver Claims User-2 Order

        return super().setUp()

    def test_valid_user(self):

        pass

    def test_valid_org(self):

        pass

    def test_valid_driver(self):

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