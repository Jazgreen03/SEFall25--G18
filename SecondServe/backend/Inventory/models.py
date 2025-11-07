from django.db import models

TYPE_PREPAREDFOOD = "prepared"
TYPE_PRODUCE = "produce"
TYPE_REFRIGERATED = "refrigerated"
TYPE_SHELFSTABLE = "stable"


class Inventory(models.Model):
    """
    Custom Inventory Model

    Contains One to Many Items through indirect association (each Item claims the Inventory)
    """

    # The name of the org that holds this Inventory
    org = models.CharField(max_length=256, unique=True)

    def has_item(self, itemName: str) -> bool:
        return self.items.filter(name=itemName).exists()

    def get_item(self, itemName: str) -> "Item":
        return self.items.filter(name=itemName).first()

    def get_items(self):
        return self.items.filter(inventory=self)


class Item(models.Model):
    """
    Custom Item model

    Linked to an Inventory by its Key
    One Inventory per Item

    """

    class ItemType(models.TextChoices):
        STABLE = TYPE_SHELFSTABLE, "Shelf Stable"
        PREPED = TYPE_PREPAREDFOOD, "Prepared"
        REFRIG = TYPE_REFRIGERATED, "Refrigerated"
        PRODUCE = TYPE_PRODUCE, "Produce"

    name = models.CharField(max_length=256)
    type = models.CharField(
        max_length=13, choices=ItemType.choices, default=TYPE_PREPAREDFOOD
    )
    quantity = models.IntegerField()
    expiration = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="items"
    )

    def to_dict(self) -> dict:

        expiration_str = self.expiration.strftime("%B {day}, %Y").format(
            day=self.expiration.day
        )

        dictVal = {
            "name": self.name,
            "type": self.get_type_display(),
            "quantity": self.quantity,
            "expiration": expiration_str,
        }
        return dictVal
