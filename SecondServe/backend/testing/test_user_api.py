from django.test import TestCase
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class UserViewsFullTest(TestCase):
    databases = "__all__"

    def setUp(self):
        # Create a base user for testing login, update, logout
        self.user = User.objects.create(
            username="existinguser", email="existing@example.com"
        )
        self.user.set_password("SecurePass123!")
        self.user.first_name = "Existing"
        self.user.last_name = "User"
        self.user.save()

    # ---------------- CREATE USER ----------------
    def test_create_user_success(self):
        response = self.client.post(
            "/user/create/",
            data=json.dumps(
                {
                    "username": "newuser",
                    "email": "new@example.com",
                    "password": "Password123!",
                    "first_name": "New",
                    "last_name": "User",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertEqual(response.json()["details"], "User Created and Logged in")

    def test_create_user_missing_fields(self):
        response = self.client.post(
            "/user/create/",
            data=json.dumps({"username": "missing"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)
        self.assertIn("details", response.json())

    def test_create_user_duplicate_username_email(self):
        # duplicate username
        response = self.client.post(
            "/user/create/",
            data=json.dumps(
                {
                    "username": "existinguser",
                    "email": "new@example.com",
                    "password": "Pass123!",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)
        # duplicate email
        response = self.client.post(
            "/user/create/",
            data=json.dumps(
                {
                    "username": "newuser",
                    "email": "existing@example.com",
                    "password": "Pass123!",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)

    # ---------------- LOGIN USER ----------------
    def test_login_user_success_username(self):
        response = self.client.post(
            "/user/login/",
            data=json.dumps({"username": "existinguser", "password": "SecurePass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["details"], "User logged in")

    def test_login_user_success_email(self):
        response = self.client.post(
            "/user/login/",
            data=json.dumps(
                {"email": "existing@example.com", "password": "SecurePass123!"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["details"], "User logged in")

    def test_login_user_invalid_credentials(self):
        response = self.client.post(
            "/user/login/",
            data=json.dumps({"username": "existinguser", "password": "Wrong"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        response = self.client.post(
            "/user/login/",
            data=json.dumps(
                {"email": "nonexistent@example.com", "password": "Whatever"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_login_user_missing_fields(self):
        response = self.client.post(
            "/user/login/",
            data=json.dumps({"username": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)
        response = self.client.post(
            "/user/login/",
            data=json.dumps({"password": "SecurePass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

    # ---------------- LOGOUT USER ----------------
    def test_logout_user_success(self):
        self.client.force_login(self.user)
        response = self.client.post("/user/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["details"], "User Logged Out")

    def test_logout_user_not_logged_in(self):
        response = self.client.post("/user/logout/")
        self.assertEqual(response.status_code, 400)

    # ---------------- UPDATE USER ----------------
    def test_update_user_success(self):
        self.client.force_login(self.user)
        response = self.client.put(
            "/user/update/",
            data=json.dumps({"attribute": "first_name", "new_value": "Updated"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["details"], "Attribute Updated")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_user_invalid_attribute(self):
        self.client.force_login(self.user)
        response = self.client.put(
            "/user/update/",
            data=json.dumps({"attribute": "unknown", "new_value": "val"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

    def test_update_user_missing_fields(self):
        self.client.force_login(self.user)
        response = self.client.put(
            "/user/update/",
            data=json.dumps({"attribute": "first_name"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 406)

    def test_update_user_invalid_json(self):
        self.client.force_login(self.user)
        response = self.client.put(
            "/user/update/", data="invalid json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_update_user_not_logged_in(self):
        response = self.client.put(
            "/user/update/",
            data=json.dumps({"attribute": "first_name", "new_value": "Updated"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    # ---------------- GET USER INFO ----------------
    def test_get_user_info_success(self):
        self.client.force_login(self.user)
        response = self.client.get("/user/info/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "existinguser")
        self.assertEqual(data["email"], "existing@example.com")

    def test_get_user_info_not_logged_in(self):
        response = self.client.get("/user/info/")
        self.assertEqual(response.status_code, 400)

    # ---------------- HTTP METHOD TESTS ----------------
    def test_methods_not_allowed(self):
        # GET on login
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 405)
        # GET on create
        response = self.client.get("/user/create/")
        self.assertEqual(response.status_code, 405)
        # POST on getUserInfo
        response = self.client.post("/user/info/")
        self.assertEqual(response.status_code, 405)
        # POST on update
        response = self.client.post("/user/update/")
        self.assertEqual(response.status_code, 405)
