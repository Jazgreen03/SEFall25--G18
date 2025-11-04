from django.db import models
from User.models import User
from Inventory.models import Item
from Organization.models import Organization

STATUS_PLACED = "placed"
STATUS_PREP = "preparing"
STATUS_READY = "ready"
STATUS_TRANSIT = "in transit"
STATUS_DELIVERED = "delivered"

class Order(models.Model):
    """
    Custom Order model

    Utilizes the following data points
    * Name (name of Order)
    * Recipient (User that placed order)
    * associatedOrg (Organization responsible for Order)
    * orderID (Publicly facing Order Number)
    * status (Status of the Order)
    * driver (Driver who claims Order)
    * driverAssigned (Boolean on if Order has been claimed by Driver)
    
    Items will reference the Order in a similar way that Items reference Inventory

    """

    class StatusTypes(models.TextChoices):
        PLACED = STATUS_PLACED, "Order Placed"
        PREPARING = STATUS_PREP, "Order being Prepared"
        READY = STATUS_READY, "Order Ready for Pickup"
        TRANSIT = STATUS_TRANSIT, "Order in Transit"
        DELIVERED = STATUS_DELIVERED, "Order Delivered"

    name = models.CharField(max_length=100)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    associatedOrg = models.ForeignKey(Organization, on_delete=models.CASCADE)
    orderID = models.IntegerField(unique=True, auto_created=True)
    status = models.CharField(max_length=25, choices=StatusTypes.choices, default=STATUS_PLACED)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    driverAssigned = models.BooleanField(default=False)

    def get_items(self):
        self.items.filter(associatedOrder=self)


class orderItem(models.Model):
    """
    Custom Order Item model

    Utilizes the following data points
    * associatedItem (The Item that has been ordred)
    * associatedOrder (Order this item is apart of)
    * numOfItem (Quantity of Item in Order)
    """
    associatedItem = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="items")
    associatedOrder = models.ForeignKey(Order, on_delete=models.CASCADE)
    numOfItem = models.IntegerField(default=1)