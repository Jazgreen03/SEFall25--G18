from django.db import models
from Inventory.models import Inventory

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

class Organization(models.Model):
    """
    Custom Inventory Model

    Contains One to Many Items through indirect association (each Item claims the Inventory)
    """

    # The ID of the org that holds this Inventory
    name = models.CharField(max_length=256)

    # What type of organization it is
    orgType = models.CharField(choices=TYPE_CHOICES, default=TYPE_OTHER)

    # Where the organization is located
    location = models.CharField(unique=True)

    # The associated inventory
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)