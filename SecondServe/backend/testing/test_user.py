from django.test import SimpleTestCase, RequestFactory
import User.views as UserAPI


class UserCreation(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_valid_creation(self):
        # Same request setup as before
        request = self.factory.post(
            "/user/create/",
            data={
                "first_name": "Caleb",
                "last_name": "Twigg",
                "username": "Twiggy",
                "email": "wctwigg@ncsu.edu",
                "password": "TotallySecure123!",
            },
        )

        response = UserAPI.createUser(request)
        self.assertEqual(response.status_code, 201)
