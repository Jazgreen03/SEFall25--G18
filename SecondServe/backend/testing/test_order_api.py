from django.contrib.auth import get_user_model
from django.test import TestCase
import json

User = get_user_model()

class testGetAvailableItems(TestCase):

    def setUp(self):

        # Create Organization with three items in their inventory

        return super().setUp()

    def test_invalid_user(self):
        # Not logged in
        response = self.client.get("/items/basicOrg/")
        self.assertEqual(response.status_code, 400)

        # Driver

        # Org but not creator

        pass


    def test_invalid_org(self):

        # Org doesnt exist

        pass


    def test_valid_get(self):

        pass

class testPlaceOrder(TestCase):

    def setUp(self):

        # Create Organization with three items in their inventory


        return super().setUp()
    
    def test_invalid_user(self):
        # Not logged in

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

class testGetActiveOrders(TestCase):

    def setUp(self):

        # Create Organization with three items in their inventory
        # Driver has two claimed orders
        # User has one claimed order
        # Organization has three orders

        return super().setUp()

    def test_invalid_user(self):
        # Not logged in

        pass

    def test_valid_user(self):

        pass

    def test_valid_org(self):

        pass

    def test_valid_driver(self):

        pass

class testGetOpenOrders(TestCase):

    def setUp(self):

        # Create Organization with three items in their inventory
        # Create three orders
        # Driver A claims 1 order
        # Driver B sees 2 open orders

        return super().setUp()

    def test_invalid_user(self):
        # Not logged in

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