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

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    associatedOrg = models.ForeignKey(Organization, on_delete=models.CASCADE)
    orderID = models.IntegerField(unique=True, auto_created=True)
    status = models.CharField(max_length=25, choices=StatusTypes.choices, default=STATUS_PLACED)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    driverAssigned = models.BooleanField(default=False)

    def get_items(self):
        self.items.filter(associatedOrder=self)

    def get_description(self):
        allItems = self.items.filter(associatedOrder=self)
        numItems = 0

        items = []

        for item in allItems:
            numItems += item.numOfItem

            orgItem = item.associatedItem

            itemDescription = {
                "Name": orgItem.name,
                "Quantity": item.numOfItem
            }
            items.append(itemDescription)

        description = {
            "Number of Items": numItems,
            "Items": items
        }

        return description

    def get_simple(self):
        return {
            "OrderID": self.orderID,
            "Destination": self.recipient.get_first_name(),
            "Organization": self.associatedOrg.name,
            "Current Status": self.status
        }

    def get_order_details_driver(self):
        recpName = self.recipient.get_first_name()
        orgName = self.associatedOrg.name
        description = self.get_description()

        return {
            "Order ID": self.orderID,
            "Status": self.status,
            "Customer": recpName,
            "Organization": orgName,
            "Description": description
        }
    
    def get_order_details_org(self):
        description = self.get_description()

        if (self.driverAssigned):
            driverStatus = self.driver.get_first_name() & " is assigned to Order"
        else:
            driverStatus = "No Assigned Driver"

        return {
            "Order ID": self.orderID,
            "Status": self.status,
            "Driver Status": driverStatus,
            "Description": description
        }
    
    def get_order_details_user(self):
        description = self.get_description()
        orgName = self.associatedOrg.name

        if (self.driverAssigned):
            driverStatus = self.driver.get_first_name() & " is assigned to Order"
        else:
            driverStatus = "No Assigned Driver"

        return {
            "Order ID": self.orderID,
            "Status": self.status,
            "Organization": orgName,
            "Driver Status": driverStatus,
            "Description": description
        }
    
    def get_order_details_admin(self):
        description = self.get_description()
        recpName = self.recipient.get_full_name()
        orgName = self.associatedOrg.name

        if (self.driverAssigned):
            driverStatus = self.driver.get_full_name()
        else:
            driverStatus = "No Assigned Driver"

        return {
            "Order ID": self.orderID,
            "Status": self.status,
            "Organization": orgName,
            "Customer": recpName,
            "Driver Status": driverStatus,
            "Description": description
        }
    


class OrderedItem(models.Model):
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