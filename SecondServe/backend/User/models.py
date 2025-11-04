from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models, IntegrityError
from django.utils import timezone

ROLE_USER = "user"
ROLE_DRIVER = "driver"
ROLE_ORGANIZATION = "organization"
ROLE_ADMIN = "admin"

ROLE_CHOICES = (
    (ROLE_USER, "User"),
    (ROLE_DRIVER, "Driver"),
    (ROLE_ORGANIZATION, "Organization"),
    (ROLE_ADMIN, "Admin"),
)


class UserManager(DjangoUserManager):
    """
    Custom manager for the User model.
    Handles creation of regular users and superusers with email as the unique identifier.
    """

    def create_user(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ):
        """
        Create and return a regular user with email and password.

        :param email: User email
        :type email: str
        :param password: User password
        :type password: str or None
        :param extra_fields: Additional fields such as role, first_name, last_name
        :return: Created user
        :rtype: User
        """

        if not username and not email:
            raise ValueError("Username and/or Email are required.")

        if email:
            email = self.normalize_email(email)

        if not username and email:
            username = email

        extra_fields.setdefault("role", ROLE_USER)

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
        if username is None and email is None:
            raise ValueError("Must have either Username or Email")

        if password is None:
            raise ValueError("Superuser must have a password.")

        if username is None:
            username = email

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
    Custom User model using email as the unique identifier.
    Includes role-based access and convenience methods.

    Abstract User already includes the following fields:
    -> Username
    -> First_Name
    -> Last_Name
    -> is_active
    -> date_joined
    """

    email = models.EmailField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ROLE_USER)

    is_staff = models.BooleanField(default=False)

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
    def get_email(self) -> str | None:
        return self.email

    def get_role(self) -> str:
        return self.role

    def get_username(self) -> str:
        return self.username

    def get_first_name(self) -> str:
        return self.first_name

    def get_last_name(self) -> str:
        return self.last_name

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
