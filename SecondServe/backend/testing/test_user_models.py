from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class TestUserModel(TestCase):
    # ---------- Creation and defaults ----------

    def test_user_creation_default_role(self):
        user = User.objects.create_user(
            username="defaultuser", email="default@example.com", password="testpass123"
        )
        self.assertEqual(user.role, "user")
        self.assertEqual(user.username, "defaultuser")
        self.assertEqual(user.email, "default@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_creation_with_custom_role(self):
        user = User.objects.create_user(
            username="supplierjoe",
            email="supplier@example.com",
            password="pw123",
            role="supplier",
        )
        self.assertEqual(user.role, "supplier")

    # def test_create_user_missing_username_raises_error(self):
    #     with self.assertRaises(TypeError):
    #         User.objects.create_user(email="no_username@example.com", password="pw123")

    # def test_create_user_missing_email_raises_error(self):
    #     with self.assertRaises(TypeError):
    #         User.objects.create_user(username="nouser", password="pw123")

    def test_create_user_missing_password_creates_unusable(self):
        user = User.objects.create_user(
            username="nopass", email="nopass@example.com", password=None
        )
        self.assertFalse(user.has_usable_password())

    def test_duplicate_username_raises_integrity_error(self):
        User.objects.create_user("dupe", "dupe@example.com", "pw123")
        with self.assertRaises(IntegrityError):
            User.objects.create_user("dupe", "different@example.com", "pw123")

    def test_duplicate_email_raises_integrity_error(self):
        User.objects.create_user("user1", "same@example.com", "pw123")
        with self.assertRaises(IntegrityError):
            User.objects.create_user("user2", "same@example.com", "pw123")

    # ---------- Setters and Getters ----------

    def test_getters_and_setters_functional(self):
        user = User.objects.create_user("john", "john@example.com", "pw123")
        user.set_email("newjohn@example.com")
        user.set_role("driver")
        user.set_username("johnny")
        user.set_password("newpw")

        assert user.get_email() == "newjohn@example.com"
        assert user.get_role() == "driver"
        assert user.get_username() == "johnny"
        assert user.check_password("newpw")

    def test_set_password_hashes_value(self):
        user = User(username="hasher", email="hasher@example.com")
        user.set_password("plain")
        assert user.password != "plain"
        assert user.check_password("plain")

    # ---------- getUserInfo ----------

    def test_get_user_info_contains_expected_fields(self):
        user = User.objects.create_user("info", "info@example.com", "pw123")
        info = user.getUserInfo()
        assert set(info.keys()) == {"email", "username"}
        assert info["email"] == "info@example.com"
        assert info["username"] == "info"

    # ---------- updateAttribute ----------

    def test_update_attribute_email(self):
        user = User.objects.create_user("alex", "alex@example.com", "pw123")
        updated = user.updateAttribute("email", "newalex@example.com")
        assert updated.email == "newalex@example.com"

    def test_update_attribute_username(self):
        user = User.objects.create_user("chris", "chris@example.com", "pw123")
        updated = user.updateAttribute("username", "newchris")
        assert updated.username == "newchris"

    def test_update_attribute_password(self):
        user = User.objects.create_user("lee", "lee@example.com", "pw123")
        updated = user.updateAttribute("password", "newpw")
        assert updated.check_password("newpw")

    def test_update_attribute_invalid_returns_none_and_does_not_change(self):
        user = User.objects.create_user("invalid", "invalid@example.com", "pw123")
        result = user.updateAttribute("not_a_field", "someval")
        assert result is None
        assert user.username == "invalid"

    def test_update_attribute_does_not_crash_with_empty_string(self):
        user = User.objects.create_user("empty", "empty@example.com", "pw123")
        updated = user.updateAttribute("username", "")
        assert updated.username == ""

    # ---------- Role validation ----------
    def test_valid_roles(self):
        roles = ["user", "driver", "supplier", "admin"]

        for role in roles:
            user = User.objects.create_user(
                f"{role}_user", f"{role}@example.com", "pw123", role=role
            )
            self.assertEqual(user.role, role)

    def test_invalid_role_assignment_is_stored_as_is(self):
        # The database does not automatically validate choices unless via ModelForm
        user = User.objects.create_user(
            "badrole", "badrole@example.com", "pw123", role="random_role"
        )
        self.assertEqual(user.role, "random_role")  # Stored but invalid logically

    # ---------- String representations and sanity ----------

    def test_user_str_method_inherits_username(self):
        user = User.objects.create_user("tester", "tester@example.com", "pw123")
        self.assertEqual(str(user), "tester")

    # ---------- Save & reload ----------

    def test_save_and_reload_preserves_fields(self):
        user = User.objects.create_user("reload", "reload@example.com", "pw123")
        user.set_email("reload2@example.com")
        user.save()
        loaded = User.objects.get(pk=user.pk)
        self.assertEqual(loaded.email, "reload2@example.com")


class TestUserManager(TestCase):
    # ---------- create_user ----------

    def test_create_user_normalizes_email(self):
        user = User.objects.create_user("norm", "Norm@Example.Com", "pw123")
        self.assertEqual(
            user.email, "Norm@example.com"
        )  # Django normalization may lowercase

    def test_create_user_sets_default_role(self):
        user = User.objects.create_user("bob", "bob@example.com", "pw123")
        self.assertEqual(user.role, "user")

    def test_create_user_with_extra_fields(self):
        user = User.objects.create_user(
            "extra", "extra@example.com", "pw123", first_name="Bob", last_name="Ross"
        )
        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Ross")

    # ---------- create_superuser ----------

    def test_create_superuser_sets_flags(self):
        superuser = User.objects.create_superuser(
            "admin", "admin@example.com", "adminpw"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password("adminpw"))

    def test_create_superuser_missing_password_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser("admin2", "admin2@example.com", password=None)
