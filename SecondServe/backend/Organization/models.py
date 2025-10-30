from django.db import models
from Inventory.models import Inventory
from User.models import User
from django.core.exceptions import ValidationError

TYPE_FOODBANK = "foodbank"
TYPE_GROCERYSTORE = "grocery"
TYPE_RESTAURANT = "restaurant"
TYPE_OTHER = "other"

TYPE_CHOICES = (
    (TYPE_FOODBANK, "Food Bank"),
    (TYPE_GROCERYSTORE, "Grocery Store"),
    (TYPE_RESTAURANT, "Restaurant"),
    (TYPE_OTHER, "Other")
)

class OrganizationManager(models.Manager):
    # Create Organization
    def createOrganization(self, user: User, name: str, orgType: str, location: str):

        if orgType not in TYPE_CHOICES:
            raise ValidationError(f"Invalid orgType: {orgType}")

        # Create the Organizations Inventory
        inv = Inventory.objects.create(organization=name)

        # Create the Organization with all the necessary variables and save to database
        Organization.objects.create(name=name, orgType=orgType, location=location, inventory=inv, creator=user)
        

class Organization(models.Model):
    """
    Custom Inventory Model
    
    Fields:
    * Name of the Organization
    * Type of the Organization
    * Location of the Organization
    * Inventory ID for Organization
    * Creator of Organization Account

    Note: Inventory has 1 to Many Items
    """

    # The name of the org
    name = models.CharField(max_length=256, unique=True)
    # What type of organization it is
    orgType = models.CharField(max_length=30, choices=TYPE_CHOICES, default=TYPE_OTHER)
    # Where the organization is located
    location = models.CharField(max_length=256, unique=True)
    # The associated inventory
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE, related_name="organization")
    # The creator User account
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="organizations")

    # The Manager for Organization
    objects = OrganizationManager()