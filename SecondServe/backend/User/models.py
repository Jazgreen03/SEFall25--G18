from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
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


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Handles creation of regular users and superusers with email as the unique identifier.
    """

    def create_user(self, email: str, password: str | None = None, **extra_fields):
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
        if not email:
            raise ValueError("The Email field is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("role", ROLE_USER)

        try:
            user = self.model(email=email, **extra_fields)
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save(using=self._db)
            return user
        except IntegrityError as e:
            raise IntegrityError(f"Duplicate user data: {e}")

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Create and return a superuser instance.

        :param email: Superuser email
        :type email: str
        :param password: Superuser password (required)
        :type password: str
        :param extra_fields: Additional attributes for the superuser
        :type extra_fields: dict
        :return: Created superuser
        :rtype: User
        """
        if not email:
            raise ValueError("Superuser must have an email address.")
        if not password:
            raise ValueError("Superuser must have a password.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", ROLE_ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using email as the unique identifier.
    Includes role-based access and convenience methods.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []  # no username required

    objects = UserManager()

    # ===== Utility Methods =====
    def set_role(self, role: str):
        """Set the user's role."""
        if role not in dict(ROLE_CHOICES):
            raise ValueError(f"Invalid role: {role}")
        self.role = role
        self.save(update_fields=["role"])

    def update_attribute(self, attribute: str, new_value: str):
        """Dynamically update a user attribute."""
        valid_attrs = {"email", "first_name", "last_name", "password", "role"}
        if attribute not in valid_attrs:
            raise ValueError(f"Invalid attribute: {attribute}")

        if attribute == "password":
            self.set_password(new_value)
        else:
            setattr(self, attribute, new_value)
        self.save(update_fields=[attribute])

    def get_user_info(self) -> dict:
        """Return basic identifying information."""
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
        }

    def __str__(self) -> str:
        """String representation of the user."""
        return f"{self.email} ({self.role})"
