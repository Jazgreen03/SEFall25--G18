"""
Manages the API calls for any operations related to the Inventory

Current API Calls Are:
1. Get Inventory
2. Add Item to Inventory
3. Bulk Edit Inventory Items (Update)
4. Edit Item in Inventory
"""

from django.urls import path
import Inventory.views as views

urlpatterns = [
    path("", views.get_inventory),
    path("add/", views.add_to_inventory),
    path("update/", views.update_inventory),
    path("edit/", views.edit_inventory),
]
