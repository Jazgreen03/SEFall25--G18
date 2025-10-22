from django.test import SimpleTestCase, RequestFactory
from unittest.mock import patch, MagicMock
import User.views as UserAPI


class UserCreation(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("User.views.get_user_model")  # Mock get_user_model
    @patch("User.views.authenticate")  # Mock authenticate
    @patch("User.views.login")  # Mock login
    def test_valid_creation(self, mock_login, mock_authenticate, mock_get_user_model):
        # Setup a fake User class
        mock_user_class = MagicMock()
        mock_user_instance = MagicMock()
        mock_user_class.objects.create.return_value = mock_user_instance
        mock_get_user_model.return_value = mock_user_class

        # Mock authenticate to return our fake user
        mock_authenticate.return_value = mock_user_instance

        # Create a POST request
        request = self.factory.post(
            "/user/create/",
            {
                "first_name": "Caleb",
                "last_name": "Twigg",
                "username": "Twiggy",
                "email": "wctwigg@ncsu.edu",
                "password": "TotallySecure123!",
            },
        )

        # Call the view
        response = UserAPI.createUser(request)

        # Check response
        self.assertEqual(response.status_code, 201)

        # Ensure create was called with correct parameters
        mock_user_class.objects.create.assert_called_with(
            username="Twiggy",
            email="wctwigg@ncsu.edu",
            password="TotallySecure123!",
            first_name="Caleb",
            last_name="Twigg",
        )

        # Ensure login was called
        mock_login.assert_called_with(user=mock_user_instance)
