from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models, IntegrityError

ROLE_USER = "user"
ROLE_DRIVER = "driver"
ROLE_SUPPLIER = "supplier"
ROLE_ADMIN = "admin"

ROLE_CHOICES = (
    (ROLE_USER, "User"),
    (ROLE_DRIVER, "Driver"),
    (ROLE_SUPPLIER, "Supplier"),
    (ROLE_ADMIN, "Admin"),
)


class UserManager(DjangoUserManager):
    """
    Custom manager for User model.

    Handles creation of regular users and superusers with validation,
    role assignment, and duplicate entry checks.
    """

    def create_user(
        self, username: str, email: str, password: str | None = None, **extra_fields
    ):
        """
        Create and return a regular User instance.

        :param username: The username of the user
        :type username: str
        :param email: The user's email address
        :type email: str
        :param password: The user's password. If None, sets an unusable password.
        :type password: str or None
        :param extra_fields: Additional fields for the user
        :type extra_fields: dict
        :return: The created User instance
        :rtype: User
        :raises TypeError: If username or email are not strings
        :raises ValueError: If username or email are empty
        :raises IntegrityError: If username or email already exist
        """
        if not isinstance(username, str) or not isinstance(email, str):
            raise TypeError("Username and email must be strings.")

        if not username or not email:
            raise ValueError("Username and email are required.")

        extra_fields.setdefault("role", ROLE_USER)
        email = self.normalize_email(email)

        try:
            user = super().create_user(
                username=username, email=email, password=password, **extra_fields
            )
        except IntegrityError as e:
            raise IntegrityError(f"Duplicate user data: {e}")

        if password is None:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and return a superuser instance.

        :param username: Superuser username
        :type username: str
        :param email: Superuser email
        :type email: str
        :param password: Superuser password (cannot be None)
        :type password: str
        :param extra_fields: Additional fields for superuser
        :type extra_fields: dict
        :return: The created superuser
        :rtype: User
        :raises TypeError: If username or email are not strings
        :raises ValueError: If password is None or flags are invalid
        """
        if not isinstance(username, str) or not isinstance(email, str):
            raise TypeError("Username and email must be strings.")

        if password is None:
            raise ValueError("Superuser must have a password.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", ROLE_ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Adds `role` field and utility methods for role-based access and
    dynamic attribute updates.
    """

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    objects = UserManager()

    # Setters
    def set_email(self, email: str):
        """
        Set the user's email.

        :param email: New email address
        :type email: str
        """
        self.email = email

    def set_role(self, role: str):
        """
        Set the user's role.

        :param role: New role for the user
        :type role: str
        :raises ValueError: If role is not one of ROLE_CHOICES
        """
        if role not in dict(ROLE_CHOICES):
            raise ValueError(f"Invalid role: {role}")
        self.role = role

    def set_username(self, username: str):
        """
        Set the user's username.

        :param username: New username
        :type username: str
        """
        self.username = username

    def set_password(self, raw_password):
        """
        Set the user's password using Django's built-in hashing.

        :param raw_password: Plaintext password
        :type raw_password: str
        """
        return super().set_password(raw_password)

    # Getters
    def get_email(self) -> str:
        """
        Get the user's email.

        :return: Email address
        :rtype: str
        """
        return self.email

    def get_role(self) -> str:
        """
        Get the user's role.

        :return: Role string
        :rtype: str
        """
        return self.role

    def get_username(self) -> str:
        """
        Get the user's username.

        :return: Username string
        :rtype: str
        """
        return self.username

    # Utility methods
    def getUserInfo(self) -> dict:
        """
        Return basic identifying information of the user.

        :return: Dictionary with 'email' and 'username'
        :rtype: dict
        """
        return {"email": self.get_email(), "username": self.get_username()}

    def updateAttribute(self, attribute: str, newValue: str):
        """
        Dynamically update a core user attribute.

        :param attribute: Attribute name ('email', 'username', 'password', 'role')
        :type attribute: str
        :param newValue: New value to set
        :type newValue: str
        :return: Updated User instance or None if attribute invalid
        :rtype: User or None
        """
        match attribute:
            case "email":
                self.set_email(newValue)
            case "username":
                self.set_username(newValue)
            case "password":
                self.set_password(newValue)
            case "role":
                self.set_role(newValue)
            case _:
                return None

        self.save()
        return self

    def __str__(self) -> str:
        """
        Return string representation of the user.

        :return: Username string
        :rtype: str
        """
        return self.username
