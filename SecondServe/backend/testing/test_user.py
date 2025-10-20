from django.test import TestCase, RequestFactory
from User.models import User, UserManager
import User.views as UserAPI

class UserCreation(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
    
    def validCreation(self):
        firstname = "Caleb"
        lastname = "Twigg"
        username = "Twiggy"
        email = "wctwigg@ncsu.edu"
        password = "TotallySecure123!"

        # Create an instance of a POST request.
        request = self.factory.post("/user/create/")

        request.body = {
            "first_name": firstname,
            "last_name": lastname,
            "username": username,
            "email": email,
            "password": password
        }

        # Test my_view() as if it were deployed at /customer/details
        response = UserAPI.createUser(request)
        
        self.assertEqual(response.status_code, 200)
