from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

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
class User(AbstractUser):

    # Fields that come with AbstractUser
    #   -> email
    #   -> username
    #   -> password
    #   -> date_joined

    # Roles for the user are limited to the following:
        # -> user
        # -> driver
        # -> supplier
        # -> admin
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    # Setters
    def set_email(self, email: str):
        self.email = email
    
    def set_role(self, role: str):
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
    
    def get_username(self):
        return self.username
    
    # Helpful methods
    def getUserInfo(self):
    
        userDetails = {
            "email": self.get_email(),
            "username": self.get_username()
        }

        return userDetails
    
    def updateAttribute(self, attribute: str, newValue: str):
        # Change the attribute based on what it is
        match attribute:
            case "email":
                self.set_email(newValue)
            case "username":
                self.set_username(newValue)
            case "password":
                self.set_password(newValue)
            case default:
                return None
        
        # Save the updated user object
        self.save()
        return self
    
    pass


class UserManager(DjangoUserManager):
    """
    Manager of the User object which handles User creation
    """

    def create_user(self, username: str, email: str, password: str, **extra_fields):
        extra_fields.setdefault("role", ROLE_USER)
        email = self.normalize_email(email)

        return super().create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)

