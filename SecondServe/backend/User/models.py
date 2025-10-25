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
    Custom manager for User object, handles user and superuser creation.
    """

    def create_user(
        self, username: str, email: str, password: str | None = None, **extra_fields
    ):
        # Type validation
        if not isinstance(username, str) or not isinstance(email, str):
            raise TypeError("Username and email must be strings.")

        # Value validation
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

        # If password is None, Django automatically sets an unusable password,
        # but we can ensure it here explicitly for clarity.
        if password is None:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        # Type validation
        if not isinstance(username, str) or not isinstance(email, str):
            raise TypeError("Username and email must be strings.")

        # Missing password should raise ValueError (per Django conventions and test)
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
    Custom User model extending Django's AbstractUser with role support.
    """

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    objects = UserManager()

    # Setters
    def set_email(self, email: str):
        self.email = email

    def set_role(self, role: str):
        if role not in dict(ROLE_CHOICES):
            raise ValueError(f"Invalid role: {role}")
        self.role = role

    def set_username(self, username: str):
        self.username = username

    def set_password(self, raw_password):
        return super().set_password(raw_password)

    # Getters
    def get_email(self) -> str:
        return self.email

    def get_role(self) -> str:
        return self.role

    def get_username(self) -> str:
        return self.username

    # Utility methods
    def getUserInfo(self):
        """Return basic identifying information."""
        return {"email": self.get_email(), "username": self.get_username()}

    def updateAttribute(self, attribute: str, newValue: str):
        """Update one of the core user attributes dynamically."""
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

    def __str__(self):
        # The test expects only the username string
        return self.username
