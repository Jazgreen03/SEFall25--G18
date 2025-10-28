from django.db import models

TYPE_PREPAREDFOOD = "prepared"
TYPE_PRODUCE = "produce"
TYPE_REFRIGERATED = "refrigerated"
TYPE_SHELFSTABLE = "stable"

TYPE_CHOICES = (
    (TYPE_PREPAREDFOOD, "Prepared"),
    (TYPE_PRODUCE, "Produce"),
    (TYPE_REFRIGERATED, "Refrigerated"),
    (TYPE_SHELFSTABLE, "Shelf Stable")
)

class Inventory(models.Model):
    """
    Custom Inventory Model

    Contains One to Many Items through indirect association (each Item claims the Inventory)
    """

    # The name of the org that holds this Inventory
    organization = models.CharField(max_length=256, unique=True)

    def has_item(self, itemName: str) -> bool:
        return self.items.filter(name=itemName).exists()


class Item(models.Model):
    """
    Custom Item model

    Linked to an Inventory by its Key
    One Inventory per Item

    """

    name = models.CharField(max_length=256)
    type = models.CharField(max_length=13, choices=TYPE_CHOICES, default=TYPE_PREPAREDFOOD)
    quantity = models.IntegerField()
    expiration = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
